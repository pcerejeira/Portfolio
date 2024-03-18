# Project 3

## Context

The objective of this project was to identify instances of high generator current variations in specific deals. The project was initiated based on a concern raised by one of the Addvolt founders regarding high generator current variations occurring in a short period of time. The goal was to pinpoint these moments and prepare a concise presentation for sharing with Addvolt's partners and stakeholders.

To make informed decisions, it was crucial to analyze the locations where the fleet spent a significant amount of time. These places presented the highest potential for charging demand and were considered strategic for the client's expansion plans. The analysis aimed to assess the viability and costs associated with implementing charging stations in those specific locations.

## Approach

The project involved fetching and analyzing data related to generator current variations for specific deals. The following steps were taken:

1. Data Retrieval: Vehicle data relevant to the analysis was fetched from the database. Key columns included 'imei,' 'registered_at,' and 'motor_controller_current_ac.'
2. Chunked Data Processing: To handle large datasets efficiently, data was fetched in chunks of 5 days at a time. This approach allowed for the systematic analysis of extensive historical data.
3. Identifying Variations: Generator current variations were identified by computing the absolute difference between consecutive rows of 'motor_controller_current_ac.'
4. Aggregation and Summation: Variations were aggregated and summed, taking into account consecutive variations. This step aimed to identify significant variations and eliminate redundant entries.
5. Redundancy Handling: To avoid double-counting, redundant entries were systematically identified and removed from the final results.
6. Categorization: Detected variations were categorized into different ranges based on the sum of consecutive variations, providing a clear overview of their frequency and magnitude.
7. Results Storage: The analysis results were stored in a CSV file for further reference and analysis.

## Insights and Findings

This analysis successfully identified instances where generator current variations met or exceeded 20 units every 4 seconds. The categorization of variations into different ranges provided valuable insights into the frequency and magnitude of high generator current fluctuations.

These findings could be instrumental in diagnosing potential issues with the generator system, understanding their impact on vehicle performance, and implementing proactive measures to address such variations.

I invite you to explore one presentation example ([Presentation](./final_presentation_example.pptx), review the analysis, and draw your own conclusions. Please keep in mind that the data used in this example was generated for illustrative purposes and does not represent a real client use case.

Please do not hesitate to reach out for further discussions or to delve deeper into the details of this project.

---

**Disclaimer:** The project code and related information in this portfolio showcase are for illustrative purposes only and may not be executable as standalone code. Random datasets were generated as examples for the portfolio.

Visit [pcerejeira.com](https://pcerejeira.com) to explore more about my journey & feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/)!

