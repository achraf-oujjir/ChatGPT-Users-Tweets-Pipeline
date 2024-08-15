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
<br>

<a name="ingestion-cleaning"></a>
### 🧹 Data Ingestion and Cleaning

The Twitter API (Application Programming Interface) is a programming interface that allows developers to access Twitter's features and data. Using the Twitter API, we were able to collect real-time, valuable information from user tweets. Access to this API is granted through secret keys provided by a Twitter Developer account. One of the first challenges encountered was dealing with the raw format of the tweets. As shown in the screenshot below, this is a snippet of a tweet obtained from the API, illustrating the raw nature of the data.

<div align="center">
  <img src="https://github.com/achraf-oujjir/ChatGPT-Users-Tweets-Pipeline/blob/master/assets/raw_data.png" alt="raw" width="720">
</div>
<br>
We can visually identify some interesting data points, such as the tweet's timestamp, source link, language, etc. To interact with this API, we use the Tweepy library in Python. The collected tweet data required extensive cleaning to prepare it for analysis. This process involved removing irrelevant information, handling missing values, and addressing inconsistencies in the data. Key tasks included:

1. **Removing Duplicates**: Identifying and removing duplicate tweets to ensure a unique dataset.
2. **Handling Missing Values**: Filling or removing missing data entries to maintain dataset integrity.
3. **Standardizing Data**: Formatting timestamps, URLs, and other fields to ensure consistency across the dataset.
4. **Preparing tweets for sentiment analysis**: Cleaning tweets' text from emojis, hashtags, mentions, etc.

I did sentiment analysis on the tweets using a custom Python class named `TweetAnalyzer`. This class leverages the `transformers` library and utilizes the `cardiffnlp/twitter-roberta-base-sentiment` model to classify tweets as **Negative**, **Neutral**, or **Positive**.

The `TweetAnalyzer` class is designed to process multiple tweets at once. It first pre-processes the tweets by removing usernames and links to ensure cleaner input for the model. Then, it encodes the pre-processed tweets and passes them through the RoBERTa model, using softmax to calculate the sentiment scores for each tweet. This allowed us to quickly analyze the overall sentiment of a large dataset of tweets, providing valuable insights into user opinions.



<a name="sftp"></a>
### 🌐 SFTP Transfer

To transfer our CSV files from the Ubuntu VM to the Cloudera VM, we use a shell script that employs the SFTP (Secure File Transfer Protocol). This script facilitates the secure transfer of files to the remote Cloudera VM.

The shell script, named `export_script.sh`, automates the file transfer process. The script can be found here: [export_script.sh](dwh_scripts/export_script.sh)

<a name="modeling"></a>
### 🏗️ Data Modeling and DWH Design
For the design of our Data Warehouse, we opted for a ⭐ star schema architecture, following Kimball's methodology. This approach helps facilitate the organization and visualization of the data we stored for sentiment analysis of ChatGPT-related tweets.

To analyze and visualize the tweets, we designed a fact table and multiple dimension tables. After several iterations, we finalized the following architecture:

<ul>
  <li><strong>🗃️ Fact Table: <code>tweets_fact</code></strong><br>
  Stores the essential details of each tweet, such as the tweet's ID, content, and references to the associated dimensions.</li>
</ul>

<ul>
  <li><strong>📊 Dimension Tables:</strong>
    <ul>
      <li><strong>👤 <code>user_dim</code></strong>: Contains data related to the tweet's author, such as user ID, name, and profile attributes.</li>
      <li><strong>📱 <code>device_dim</code></strong>: Stores information about the operating system and device from which the tweet was posted.</li>
      <li><strong>🏷️ <code>hashtag_dim</code></strong>: Captures the hashtags associated with each tweet.</li>
      <li><strong>🧠 <code>sentiment_dim</code></strong>: Holds the sentiment analysis results for each tweet, including scores and labels (Negative, Neutral, Positive).</li>
      <li><strong>🌍 <code>location_dim</code></strong>: Provides geographical data related to the tweet's source, including country and city.</li>
      <li><strong>⏰ <code>time_dim</code></strong>: Stores the timestamp of when the tweet was posted, broken down into components such as date, hour, and minute.</li>
    </ul>
  </li>
</ul>

This ⭐ star schema enables efficient querying and aggregation of tweet data, which we leveraged for sentiment analysis and visualization in Power BI.


<a name="dwh-load"></a>
### 📦 DWH Load


<a name="visualization"></a>
### 📊 Data Visualization
