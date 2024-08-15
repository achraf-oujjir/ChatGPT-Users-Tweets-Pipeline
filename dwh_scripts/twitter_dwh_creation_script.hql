create table tweets_fact (tw_id string, tw_text string, author_id string, retweet_count int, favorite_count int,engagement_rate double, created_at string, retweet boolean, tw_url string) row format delimited fields terminated by '|';
create table time_dim (tw_id string, created_at string, ymd date, day int, month int, year int, day_of_week string, time_ string, hour int, minute int, second int) row format delimited fields terminated by '|';
create table user_dim (tw_id string, user_id string, user_name string, loc string, followers_count int, statuses_count int) row format delimited fields terminated by '|';
create table sentiment_dim (tw_id string, tw_text string, score double, neg double, neut double, pos double, general_sentiment string, sentiment string) row format delimited fields terminated by '|';
create table device_dim (tw_id string, source string, source_url string, device string, from_ string, operating_system string) row format delimited fields terminated by '|';
create table hashtag_dim (tw_id string, hashtag string, normalized_hashtag string) row format delimited fields terminated by '|';
create table location_dim (tw_id string, user_location string, city string, state string, country string, geocode string) row format delimited fields terminated by '|';


-- Skip headers:
ALTER TABLE user_dim SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE location_dim SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE sentiment_dim SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE time_dim SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE device_dim SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE tweets_fact SET TBLPROPERTIES ("skip.header.line.count"="1");
ALTER TABLE hashtag_dim SET TBLPROPERTIES ("skip.header.line.count"="1");



-- For loading data:
load data local inpath '/home/cloudera/Desktop/Twitter_Data/tweet_fact.csv' into table tweets_fact;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/device_dim.csv' into table device_dim;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/hashtag_dim.csv' into table hashtag_dim;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/location_dim.csv' into table location_dim;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/sentiment_dim.csv' into table sentiment_dim;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/time_dim.csv' into table time_dim;
load data local inpath '/home/cloudera/Desktop/Twitter_Data/user_dim.csv' into table user_dim;

-- Truncate tables:
truncate table user_dim;
truncate table location_dim;
truncate table sentiment_dim;
truncate table time_dim;
truncate table device_dim;
truncate table tweets_fact;
truncate table hashtag_dim;

-- Drop tables:
drop table user_dim;
drop table location_dim;
drop table sentiment_dim;
drop table time_dim;
drop table device_dim;
drop table tweets_fact;
drop table hashtag_dim;


