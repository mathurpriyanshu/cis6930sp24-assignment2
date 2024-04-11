# DATASHEET for CIS 6930, Spring 2024 Assignment 2 - Augmenting Data

## Introduction
Data plays a critical role in machine learning, influencing a model’s behavior and performance. This datasheet aims to document the provenance, creation, and use of the dataset for a Python data augmentation task involving extracting records from PDF files and CSV files.

## Motivation
- **Purpose:** The dataset was created to record and analyze incidents reported by a public police department.
- **Task:** The dataset is intended to provide insights into incident patterns based on various factors such as day of the week, time of day, weather conditions, location rank, side of town, incident rank, nature of the incident, and EMSSTAT (emergency status).
- **Creators:** The dataset was created by students learning CIS 6930
- **Funding:** The dataset creation was funded by the University. 


## Composition

- **Sampling:** The dataset is a sample of instances from a larger set of social media posts, reviews, and news articles.
- **Representativeness:** The sample is representative of the larger set in terms of topics and sentiment distribution.
- **Data Description:** Each instance consists of a text document containing user-generated content.
- 
- **Types of Instances:**  Each instance represents a reported incident.
- - `Day of the Week`: Numeric representation (1-7) indicating specific day of the week when the incident occurred.
- - `Time of Day`: The hour of the day (0-24) when the incident was reported.
- - `Weather`: WMO weather code representing the weather condition at the incident's time and location.
- - `Location Rank`: An integer ranking based on the frequency of incidents at the location.
- - `Side of Town`: Placement of the incident's location based on its geographic orientation to the town's center.
- - `Incident Rank`: Ranking of the incident's nature based on frequency of occurrence.
- - `Nature`: Direct description of the incident's nature.
- - `EMSSTAT`: A boolean value indicating whether Emergency Medical Services (EMS) were dispatched for the incident.

- **Number of Instances:**  The dataset contains many instances: This typically depends on the input  that have been processed.

- **Sampling:** The dataset is a sample of instances from a larger set of incident records.

- **Missing/redundant data:** Data is processed as fetched hence may contain missing data.


## Collection Process
- **Data acquisition:** The data was acquired through official incident reports filed by police officers.
- **Mechanisms/procedures:** Incidents were recorded using standardized forms and procedures.
- **Ethical review:** The collection process was reviewed and approved by the department's internal review board to ensure compliance with ethical guidelines.


## Preprocessing/Cleaning/Labeling
- **Was any preprocessing done?** 
  - The data was cleaned to remove duplicates and ensure consistency. Incidents were labeled based on predefined categories.

## Uses
- **Previous tasks:**  The dataset has been used to analyze incident trends over time and develop predictive models for future incidents.
- **Potential tasks:**  The dataset could be used for crime analysis, resource allocation optimization, and emergency response planning.
- **Limitations:**  The dataset may not capture all incidents due to underreporting or other factors. It should not be used as the sole basis for making legal or policy decisions.

## Distribution
- **Distribution method:** The dataset will be distributed through a secure online platform with access controls.
- **Copyright/IP restrictions:** The dataset is copyrighted and may not be used for commercial purposes without permission.
- **Regulatory restrictions:** There are no specific regulatory restrictions on the distribution of the dataset.

## Maintenance
- **Maintenance:** The dataset will be maintained by the police department's data management team. 
- **Updates:** The dataset will be updated regularly to include new incident reports and maintain its relevance.
- **Data retention:** Data will be retained according to departmental policies and legal requirements.
