# Battery Efficiency: Analyzing battery behavior on extreme conditions

## Context

The objective of this project was of utmost importance for Addvolt's marketing purposes and market expansion. It aimed to analyze the relationship between the temperature of different battery components and the ambient temperature in which a vehicle operates. This analysis played a crucial role in determining the viability and effectiveness of Addvolt's products in various geographic locations, including different countries with diverse climate conditions.

Understanding the impact of ambient temperature on battery efficiency allowed Addvolt to showcase the reliability and performance of their batteries even in extreme weather conditions such as scorching summers or freezing winters. By demonstrating that the batteries maintained regular and stable temperatures regardless of the ambient temperature, the Startup could confidently promote their products as suitable for a wide range of climates.


## Analysis Approach

The analysis involved the following steps:

1. **Data Retrieval:** Raw data containing battery and vehicle data, as well as location coordinates, was fetched from the database using SQLAlchemy and the `fetch_by_identification` function.

2. **Data Preprocessing:** The fetched data was processed using Pandas to rename columns and convert timestamps to appropriate formats. The data was also resampled based on a specified period to aggregate temperature readings.

3. **External API Integration:** An external API from weather.com was utilized to fetch the ambient temperature for the corresponding location where the vehicle operated. The API provided information such as temperature, relative humidity, heat index, pressure, wind direction, gust speed, precipitation, and snow accumulation.

4. **Data Analysis and Visualization:** The aggregated battery temperature data and the corresponding ambient temperature were analyzed using Pandas and Matplotlib. The analysis included computing min, max, and median temperatures for each battery component and comparing them with the ambient temperature. The data was visualized through line plots to observe trends and relationships between temperatures.

## Covered mainly

- Python
- Pandas
- Matplotlib
- SQLAlchemy
- External Api (https://api.weather.com)
- Database Queries (1.5T table size)

## Solution

The solution involved developing a Python script that implemented the analysis approach described above. The script utilized various libraries and modules, including Pandas, Matplotlib, and SQLAlchemy, to retrieve, preprocess, analyze, and visualize the data.

The script allowed for the flexibility to analyze temperature data for different batteries and battery components by specifying the vehicle identification and resampling period as input parameters. The generated plots were saved in the specified output path.

Please note that the code provided is a simplified representation and may require modifications and adaptations to work in different environments or with actual data.

Feel free to explore the code, implementation details and some outputs in the files inside the project's directory.

---

**Disclaimer:** The project code and related information in this portfolio showcase are for illustrative purposes only and may or may not be executable as standalone code.

Visit [pcerejeira.com](https://pcerejeira.com) to explore more about my journey & feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/)!

