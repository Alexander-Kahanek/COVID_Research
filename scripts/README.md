# Scripting Order and Code

The scripts should be ran in the following order:

* decompress_and_filter.py
* json_2_csv_script.py
* preprocess_flair.py
* flair_ner.py
* flair_pos.py
* flair_sent.py
* join_flair.py

The code to do so is the following:

```
run_filter()
join_json_to_csv()
preprocess_4_flair()
flair_sent()
flair_ner()
flair_pos()
join_flair_2_json()
```

# The Algorithms

These are the algorithms for the following scripts:

* decompress_and_filter.py filters through compressed json files, and create a cleaner json file.
  + ADD: total tweet count to complete.txt
  + loads in compressed json file -> decompresses file
  + loads in individual tweet and checks if it has the conditions needed to keep the tweet for further analysis
  + appends whole tweet to json file
    - structured as: {tweet}\n{tweet}\n{tweet} ... ect.

* json_2_csv_script.py takes the json file from the above script, and clean the data down into a csv file. This is used to make a quick analysis on the distribution of tweets gathered.
  + loads in a single tweet from the json file created from filter_script.py 
  + loads specific data from tweet into a dataframe format.
	- 'created_at', 'user_id_str', 'text', 'coordinates', 'place_coordinates', 'place_country', 'place_country_code', 'place_full_name', 'place_type', 'language'
  + appends tweet into a created csv file.

* The following scripts follow the same algorithm:
	+ flair_ner.py 
		- script using flair to get Named Entity Recognition from tweet texts
	+ flair_pos.py 
		- script using flair to get Part of Speech from tweet texts
	+ flair_sent.py 
		- script using flair to get Sentiment of tweet texts
	+ Algorithm:
		- load in data created from json_2_csv_script.py
		- load in given model from flair
		- iterate through df from csv file
		- save 'created_at', 'place', 'text', '[FLAIR MODEL]' into json object
		- append json object to file

* join_flair.py uses the files from the above scripts and joins them all into one csv file
	+ load in data from pos_tweets.json, ner_tweets.json, sentiment_tweets.json
	+ combines each tweet from 3 files into 1 dictionary object
	+ appends new dictionary object to combined json file, flair_joined_tweets.json
	+ converts dictionary object to csv file and outputs to flair_joined_tweets.csv

