# Ready to be discharged: Predicting hospital readmissions

## Context

The objective of this project is to develop classification models for predicting hospital readmissions. Hospital readmissions are a critical concern in healthcare, impacting both patient outcomes and healthcare costs. By accurately predicting readmissions, healthcare providers can implement preventive measures and tailor post-discharge care to reduce readmission rates and improve patient care.

## Approach

The algorithm involves the following steps:

1. **Data Exploration & Visualization:** We begin by exploring and visualizing the dataset to understand its structure and identify key patterns and trends.

2. **Data Split:** We split our data into training and validation sets.

3. **Pre-processing:** In this step, we handled duplicates, missing values, outliers, and aggregated categories, between others, to ensure the quality and integrity of the data.

4. **Feature Engineering:** Creating new variables from existing ones to improve the robustness of the model. Additionally, we encoded categorical variables and scaled numerical features to ensure uniformity and compatibility across different algorithms.

5. **Feature Selection:** Reducing the dataset complexity to identify the variables that most contribute to the predictions. 

6. **Resampling:** We experimented with both oversampling and undersampling techniques to address class imbalance and enhance the model's performance on minority classes.

7. **Modeling:** Utilizing diverse machine learning algorithms, we optimized hyperparameters to maximize F1 scores, ensuring robust predictive performance.

For a detailed explanation of each step, please refer to the [report](/machine-learning/project1/report.pdf) available in this GitHub repository.

## Covered mainly

- Python
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Imbalanced-learn (imblearn)

## Solution

The solution provided accurate predictive models for hospital readmissions, enabling healthcare providers to identify patients at risk of readmission and implement timely interventions to improve patient outcomes. By leveraging machine learning techniques and comprehensive data analysis, the solution empowered healthcare organizations to optimize resource allocation, reduce healthcare costs, and enhance the quality of patient care.

**Please note that while you should be able to find all we tested and implemented in the code, some sections may be commented out due to reasons such as not being used or being too time-consuming to execute. Additionally, the final output is the report, so the code may include observations, comments, or code snippets that are not fully cleaned or optimized for presentation purposes.**

Feel free to explore the code, report, and the dataset in the files within the project directory.



---

**Disclaimer:** The project code and related information in this portfolio showcase are for illustrative purposes only and may or may not be executable as standalone code.

Visit [pcerejeira.com](https://pcerejeira.com) to explore more about my journey & feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/pedrocerejeira/)!
