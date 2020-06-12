# COVID Reasearch Project

This project is currently being worked on.

# Files

All the data is stored on a virtual machine, so it will not be posted to github.

* filter_scripts.py is a script I made to filter through compressed json files, and create a cleaner json file.
  + loads in compressed json file -> decompresses file
  + loads in individual tweet and checks if it has the conditions needed to keep the tweet for further analysis
  + appends whole tweet to json file
    - structured as: {tweet}\n{tweet}\n{tweet} ... ect.

* json_2_csv_script.py is a script I made to take the json file from the above script, and clean the data down into a csv file. This is used to make a quick analysis on the distribution of tweets gathered.
  + loads in a single tweet from the above created json file.
  + loads specific data from tweet into a dataframe format.
  + appends tweet into a created csv file.

* flair_script.py is a script built to run the tweets through flairs' models and output the data into a json file
  + need to seperate this script into one script per flair model
  + need to build a script to take finished json files from above, and combine into one big json file

+ generate_graphs.py is a script made to get a quick analysis from the above json file created from the above.
  + loads in tweets from json file and saves to list of dictionaries.
  + functions will transfer data from lists to: 
    - a string, counted word dictionaries, ect.
  + pushes specific requirements to a wordcloud graphs
    - wordclouds are saved in a new folder as png
  + pushes word count dictionaries to text documents
  
MORE TO COME!
