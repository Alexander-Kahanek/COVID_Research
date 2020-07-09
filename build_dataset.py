# order to run
from scripts.decompress_and_filter import *
from scripts.json_2_csv import *
from scripts.preprocess_flair import *
from scripts.flair_ner import *
from scripts.flair_pos import *
from scripts.flair_sent import *
from scripts.join_flair import *

# decompresses <file>.jsonl.gz file
# filters through tweets and saves json file
run_filter()

# takes json file and converts it to a csv file
join_json_to_csv()

# takes csv file and preprocesses the data
# and saves data as a new csv to be ran through flair
preprocess_4_flair()

# runs above csv through flair models
flair_sent()
flair_ner()
flair_pos()

# joins files from above flair modeling, runs
# text through spaCy and outputs final csv file
# fix spacy model and english loads
# join_flair_2_json()
