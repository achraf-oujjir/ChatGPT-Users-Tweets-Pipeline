<div align="center">
  <h1>ChatGPT Users Tweets Analysis Pipeline</h1>
  <br>
  <br>
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/assets/banner.png" alt="architecture" width="720">
  <br>
  <br>
  <p>Unlocking insights from ChatGPT Users' Tweets</p>
</div>

## 📝 Table of Contents

1. [ Project Overview ](#introduction)
2. [ Project Architecture ](#architecture)


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
## 📝 Project Architecture

<div align="center">
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/architecture.png" alt="architecture" width="720">
</div>
