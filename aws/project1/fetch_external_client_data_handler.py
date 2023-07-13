import time
from datetime import datetime
import logging
import json
import pysftp
import boto3
from flask import Response
import os

# Imported functions included in the end of this file for a simpler portfolio structure
# from utils.authenticate_sftp import authenticate_sftp 


# List of jobs for data retrieval: Holds information about clients, their data retrieval methods, and file paths. 
# Manually updated for new clients.

jobs = [
    {
        "client": "Client_X",  # Placeholder for the client identifier
        "method": {
            "sftp": {
                "host": "sftp.example.com",  # Placeholder for the SFTP host
                "username": "example_user",  # Placeholder for the SFTP username
                "password": os.getenv("CLIENT_X_SFTP_PASSWORD"),  # Placeholder for the SFTP password
            }
        },
        "paths": ["/example/path/to/file.csv"],  # Placeholder for the file path(s) to retrieve
    }
]

class FetchExternalClientDataRequest:
    """
    Fetch client data, using different methods.
    """

    def __init__(self):
        start_time = time.time()
        # Create logger instance for this request
        self.logger = logging.getLogger("job.fetch_external_client_data")

        for job_entry in jobs:
            self.fetch_data(job_entry)

        # Logging elapsed time
        elapsed_time = time.time() - start_time
        self.logger.info(f"Took {elapsed_time:.2f} sec.")

    def fetch_data(self, job_entry):
        start_time = datetime.now()

        # Formatting datetime to include in the saved file's name
        formatted_datetime = start_time.strftime("%d_%m_%Y")

        # Saving transfer data for logging purposes
        transference_success = 0
        transference_error = 0

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Disable host key checking

        # S3 access details
        AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY") # Placeholder for the AWS Access Key
        AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY") # Placeholder for the AWS Secret Key

        # S3 bucket details
        s3_bucket_name = "backups-example"

        # Check if the 'method' field exists and contains implemented methods ('sftp' implemented for now)
        if "method" not in job_entry or "sftp" not in job_entry["method"]:
            self.response = {
                "status": "error",
                "message": "No valid method configuration found in the job entry.",
            }
            return

        sftp_config = job_entry["method"]["sftp"]

        # Authenticate and retrieve file contents and paths
        file_contents, file_paths = authenticate_sftp(sftp_config, cnopts, job_entry["paths"])

        for file_content, file_path in zip(file_contents, file_paths):
            try:
                # Get the filename from the file path
                filename = os.path.basename(file_path)

                # Including the datetime and the filename in the S3 saved file, so we keep past files
                s3_key_w_date = f"company{job_entry['client']}/{formatted_datetime}_{filename}"
                
                # File saved without the date, rewriting itself every day, so we have a path that is always updated and eases analysis
                s3_key = f"company{job_entry['client']}/{filename}"

                # Upload the file content to S3
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                )
                s3_client.put_object(
                    Body=file_content,
                    Bucket=s3_bucket_name,
                    Key=s3_key_w_date,
                )
                s3_client.put_object(Body=file_content, Bucket=s3_bucket_name, Key=s3_key)

                self.logger.info(f"Data fetched and saved successfully for file: {file_path}.")

                transference_success += 1

            except Exception as e:
                self.logger.error(f"Failed to store data in S3 for file: {file_path}. Error: {str(e)}")

                transference_error += 1

        self.response = {
            "message": f"Successfully stored data in S3 for {transference_success} files. Failed the transfer of {transference_error} files.",
        }

    def get_response(self):
        return Response(json.dumps(self.response), mimetype="application/json")

# ------

def authenticate_sftp(sftp_config, cnopts, paths):
    # Create logging instance
    logger = logging.getLogger(f"services.authenticate_sftp")

    # Check if the required SFTP connection details are provided
    if "host" not in sftp_config or "username" not in sftp_config or "password" not in sftp_config:
        return None, None

    sftp_host = sftp_config["host"]
    sftp_username = sftp_config["username"]
    sftp_password = sftp_config["password"]

    try:
        # Establish SFTP connection
        with pysftp.Connection(
            host=sftp_host,
            username=sftp_username,
            password=sftp_password,
            cnopts=cnopts,
        ) as sftp:
            # Return an array with contents from all files and file paths in the server
            file_contents = []
            file_paths = []

            for file_path in paths:
                # Read file content
                file_content = sftp.open(file_path, "rb").read()

                if file_content is None:
                    print(f"Failed to fetch data from SFTP server for file: {file_path}.")
                else:
                    file_contents.append(file_content)
                    file_paths.append(file_path)

            return file_contents, file_paths

    except Exception as e:
        # Log the error message
        logger.error(f"Failed to fetch data from SFTP server: {str(e)}")
        return None, None
