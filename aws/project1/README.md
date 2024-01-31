# Project 1

## Context

The objective of this project was to retrieve and store client data from food transportation companies. Each company provided a daily schedule in the form of a CSV file, which described the routes for each truck in their fleet for that day.

The data retrieval process was a crucial component in building a smart and autonomous solution for the company's charging practices. By fetching the schedule files from the companies at the beginning of each day, we ensured the availability of up-to-date and accurate data for analysis and optimization.

The initial implementation focused on connecting to the client servers via SFTP to fetch the schedule files. However, the code was designed with the flexibility to accommodate other companies with different access methods or multiple files per day, although those aspects were not fully implemented at this stage due to the lack of immediate necessity.

The developed code was tailored to address the specific requirements of the food transportation industry, while considering potential scalability and adaptability to accommodate future enhancements and varying data sources.

## Technologies and Libraries Used

- Python: The main programming language used for developing the script.
- `pysftp`: A Python library for secure file transfer protocol (SFTP) operations.
- `boto3`: The AWS SDK for Python, used for interacting with AWS services, including S3.
- `logging`: Python's built-in logging module, used for recording information and errors during script execution.

## Solution

To achieve the data retrieval and storage, I developed a Python script utilizing the pysftp library for secure file transfer protocol (SFTP) operations and the boto3 library to establish a connection with AWS S3. The script was integrated into a larger system, which included a task scheduler to automate the daily execution.

The script followed a step-by-step process, which included:

- Connect to the client server via SFTP using secure credentials (saved in the machine running the task scheduler as environment variables).
- Fetch available files from the server.
- Establish a connection with AWS S3 using AWS credentials.
- Upload the retrieved files to the designated AWS S3 bucket.

Throughout the code, I implemented logging using the `logging` library to record relevant information and errors during script execution.


Feel free to explore the project code and implementation details in the files inside the project's directory.

---

**Disclaimer:** The project code and related information in this portfolio showcase are for illustrative purposes only and may not be executable as standalone code.

Connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/) to learn more about my background, experience, and potential collaboration opportunities.

