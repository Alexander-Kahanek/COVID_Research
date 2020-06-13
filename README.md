# COVID Reasearch Project

This project is currently being worked on.

# Files

All the data is stored on a virtual machine due to size, so it will not be posted to github.

## 1_process_data

Scripts are to be ran in the below order, hyperparameters can be changed in the top of the .py file, or the script can be imported as a function.

* filter_script.py is a script I made to filter through compressed json files, and create a cleaner json file.
  + loads in compressed json file -> decompresses file
  + loads in individual tweet and checks if it has the conditions needed to keep the tweet for further analysis
  + appends whole tweet to json file
    - structured as: {tweet}\n{tweet}\n{tweet} ... ect.

* json_2_csv_script.py is a script I made to take the json file from the above script, and clean the data down into a csv file. This is used to make a quick analysis on the distribution of tweets gathered.
  + loads in a single tweet from the json file created from filter_script.py 
  + loads specific data from tweet into a dataframe format.
	- 'created_at', 'user_id_str', 'text', 'coordinates', 'place_coordinates', 'place_country', 'place_country_code', 'place_full_name', 'place_type', 'language'
  + appends tweet into a created csv file.

## 2_flair_scripts

Scripts are to be ran in the below order, hyperparameters can be changed in the top of the .py file, or the script can be imported as a function.

* flair_ner.py - script using flair to get Named Entity Recognition from tweet texts
* flair_pos.py - script using flair to get Part of Speech from tweet texts
* flair_sent.py - script using flair to get Sentiment of tweet texts

They all follow this algorithm:

* load in data created from json_2_csv_script.py
* load in given model from flair
* iterate through df from csv file
* save 'created_at', 'place', 'text', '[FLAIR MODEL]' into json object
* append json object to file

NEED script to combine all 3 json created from above, into singular dictionaries.

## analysis

* no_place.ipynb
	+ NOT AN OFFICIAL WRITTEN ANALYSIS
	+ this is an internal analysis to test the distribution of tweets from filtering with only geo location coordinates
	
* yes_place.ipynb
	+ NOT AN OFFICIAL WRITTEN ANALYSIS
	+ this is an internal analysis to test the distribution of tweets from filtering with place information available

* flair_analysis.ipynb
	+ NOT AN OFFICIAL WRITTEN ANALYSIS
	+ this is an internal analysis to test a sample of the data being ran through flair, then generating wordclouds for a quick analysis.

+ generate_graphs.py is a script made to get a quick analysis from the above json file created from the above.
  + loads in tweets from json file and saves to list of dictionaries.
  + functions will transfer data from lists to: 
    - a string, counted word dictionaries, ect.
  + pushes specific requirements to a wordcloud graphs
    - wordclouds are saved in a new folder as png
  + pushes word count dictionaries to text documents
  
MORE TO COME!
