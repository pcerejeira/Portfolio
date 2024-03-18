# Project 2

## Context

The objective of this project was to evaluate a new investment opportunity in the Electric Vehicle (EV) charging infrastructure. The client, a prominent player in the EV industry, wanted to identify the optimal locations for building new EV charging stations based on the impact on their fleet operations.

To make informed decisions, it was crucial to analyze the locations where the fleet spent a significant amount of time. These places presented the highest potential for charging demand and were considered strategic for the client's expansion plans. The analysis aimed to assess the viability and costs associated with implementing charging stations in those specific locations.

## Approach

The project involved analyzing the fleet's data to identify the stops where vehicles spent the most time. The analysis considered factors such as the duration of the stops, frequency of visits, and the type of activities performed at each location. By identifying the key areas where the fleet was frequently stopped, the client could prioritize these locations for further analysis and investment decisions.

The project code fetched data related to vehicle operations from the client's database. The code focused on retrieving information about the stops (non-facilities) made by the vehicles within a specified time range.

The code followed the following steps:

1. Fetching vehicle data for analysis.
2. Iterating over 15-day intervals within the specified time range to retrieve detailed vehicle operation information.
3. Consolidating the fetched data into a single dataframe.
4. Performing data cleaning and manipulation to prepare the data for analysis.
5. Grouping the stops by vehicle, latitude, and longitude and calculating the number of occurrences.
6. Filtering out non-significant stops and default/error values.
7. Considering nearby coordinates within a certain range as the same location and aggregating the data accordingly.
8. Calculating the total occurrence percentage and generating Google Maps links for each location.
9. Saving the results in a CSV file.

In addition to the code, the project included a presentation that showcased the analysis results. The presentation went beyond the technical aspects and focused on the business implications of the investment opportunity. It provided insights into the potential profitability, expenses, and feasibility of implementing EV charging stations in the identified locations. The presentation served as a valuable resource for decision-making and further exploration of the investment opportunity. 

While the presentation file contains sensitive information from the client related to the business, it cannot be shared publicly. However, I am more than willing to discuss the analysis, provide insights, and explain the logic and thought process behind the data-driven investment analysis. 

Please feel free to reach out to me for further discussions and to explore the details of the project.

---

**Disclaimer:** The project code and related information in this portfolio showcase are for illustrative purposes only and may not be executable as standalone code. Random locations where generated as example for the portfolio.

Visit [pcerejeira.com](https://pcerejeira.com) to explore more about my journey & feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/)!

