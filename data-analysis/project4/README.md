# Project 4

## Context

The Custom Plot functionality in our application had been exhibiting considerable delays, raising concerns within the team. The primary hypothesis was that middlewares such as "rate limiter" and "slowdown" might be responsible for the sluggish performance, especially when the API was handling substantial requests linked to the raw-records-for-plot endpoint. This project was triggered by the team leader's observations, aiming to diagnose and tackle the potential bottlenecks, with the broader goal of evaluating whether the constraints placed on the Custom Plot functionality needed adjustment.

## Approach

To get to the heart of the issue, the following steps were initiated:

1. Data Retrieval: API logs related to the Custom Plot functionality were extracted from the database, focusing on columns like 'timestamp,' 'path,' 'time_elapsed,' and 'permissions.'
2. Chunked Data Processing: Given the volume of logs, data was processed in chunks of 5 days to maintain efficiency and ensure comprehensive analysis over an extended period.
3. Middleware Impact Analysis: We assessed the impact of "rate limiter" and "slowdown" middlewares by contrasting the elapsed time with the expected time for various requests.
4. Identifying Problematic Requests: Requests with significant delays were isolated to understand their underlying causes.
5. Redundancy Handling: To offer an unclouded picture, we filtered out redundant entries and outliers that might distort the results.
6. Correlation Analysis: A correlation study was launched to determine the relationship between request size/frequency and the observed latencies.
7. Recommendations and Storage: The insights yielded actionable recommendations, which, along with the results, were archived in a CSV file for future reference.

## Insights and Foundings

The period of scrutiny spanned from 1st January 2023 to 5th September 2023. Please find an example of the conclusion drawn from this analysis here ([Presentation](./Conclusion.pdf))

In summary, while the rate limiter and slowdown middlewares had an undeniable role in influencing the request-processing time, the intrinsic nature of the requests, especially those involving intricate variables, seemed to be a considerable determinant of the observed delays.

The insights garnered here offer a foundational understanding, serving as a launchpad for optimizing our API's performance, refining the user experience, and potentially revisiting the permissions and data access policies.

If you have any questions, wish to discuss the findings further, or delve into any other aspects of our projects, please don't hesitate to reach out.

---

**Disclaimer:** The details presented in this portfolio highlight are for demonstrative purposes and may not reflect a real-world scenario. The datasets used here are fabricated examples.

Connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/) to learn more about my background, experience, and potential collaboration opportunities.

