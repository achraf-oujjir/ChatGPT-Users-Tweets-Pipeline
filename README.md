<div align="center">
  <h1>ChatGPT Users Tweets Analysis Pipeline</h1>
  <br>
  <br>
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/assets/banner.png" alt="banner" width="720">
  <br>
  <br>
  <p>Unlocking insights from ChatGPT Users' Tweets</p>
</div>

## 📝 Table of Contents

1. [ Project Overview ](#introduction)
2. [ Project Architecture ](#architecture)
3. [ Data Ingestion and Cleaning ](#ingestion-cleaning)
4. [ SFTP Transfer ](#sftp)
5. [ Data Modeling and Design ](#modeling)
6. [ DWH Load ](#dwh-load)
7. [ Data Visualization ](#visualization)

<hr>

<a name="introduction"></a>
## Project Overview 🔬:

### Goal 🎯:

This project aims to provide a deep analysis of user feedback on ChatGPT, using data sourced from Twitter. The objective is to ingest, clean, model and visualize user opinions and discussions to uncover trends and insights regarding ChatGPT. By analyzing this social media data, we can better understand user sentiment, highlighting key areas such as popular features, common frustrations, and suggestions for improvement. The project features an end-to-end data pipeline, storing the data in a structured Hive datawarehouse, and ultimately creating insightful visualizations.

### Steps 🛠️:

The project kicks off by using Python to connect with the Twitter API and extract tweets containing the term "ChatGPT." These tweets are filtered to focus on user feedback, ranging from positive experiences to areas of concern. After collection, the raw data undergoes cleaning, handle missing values and eliminate duplicates.

The processed data is then organized into a star schema, composed of fact and dimension tables, for optimized querying and analysis. CSV files with the cleaned data are securely transferred from an Ubuntu virtual machine to a Cloudera virtual machine using the SFTP protocol. On the Cloudera machine, the data is ingested into a Hive data warehouse, where it is structured and stored in tables.

With the data securely housed in Hive, Power BI is connected to access the Hive data warehouse on Cloudera. Within Power BI, an interactive dashboard is built, allowing for exploration of user sentiment, trending topics, and key insights around ChatGPT feedback. This visualization provides stakeholders with a clear view of user perceptions, helping to guide future improvements and feature development.

<a name="architecture"></a>
### 📝 Project Architecture

<div align="center">
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/architecture.png" alt="architecture" width="720">
</div>


<a name="ingestion-cleaning"></a>
### 🧹 Data Ingestion and Cleaning

The Twitter API (Application Programming Interface) is a programming interface that allows developers to access Twitter's features and data. Using the Twitter API, we were able to collect real-time, valuable information from user tweets. Access to this API is granted through secret keys provided by a Twitter Developer account.

One of the first challenges encountered was dealing with the raw format of the tweets. As shown in the screenshot below, this is a snippet of a tweet obtained from the API, illustrating the raw nature of the data.

<div align="center">
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/raw_data.png" alt="raw" width="720">
</div>

We can visually identify some interesting data points, such as the tweet's timestamp, source link, language, etc. To interact with this API, we use the Tweepy library in Python.

The collected tweet data required extensive cleaning to prepare it for analysis. This process involved removing irrelevant information, handling missing values, and addressing inconsistencies in the data. Key tasks included:

1. **Removing Duplicates**: Identifying and removing duplicate tweets to ensure a unique dataset.
2. **Handling Missing Values**: Filling or removing missing data entries to maintain dataset integrity.
3. **Standardizing Data**: Formatting timestamps, URLs, and other fields to ensure consistency across the dataset.
4. **Preparing tweets for sentiment analysis**: Cleaning tweets' text from emojis, hashtags, mentions, etc.



<a name="sftp"></a>
### 🌐 SFTP Transfer

<a name="modeling"></a>
### 🏗️ Data Modeling and DWH Design

<a name="dwh-load"></a>
### 📦 DWH Load


<a name="visualization"></a>
### 📊 Data Visualization
