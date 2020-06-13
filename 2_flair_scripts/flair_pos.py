import pandas as pd
import json
from flair.data import Sentence
from flair.models import SequenceTagger

##########################
# HYPERPARAMETERS ########
FIN = "filtered/tweets.csv"
FOUT = "flair/pos_tweets.json"
##########################

def flair_pos(FIN, FOUT):
    # function used to take csv tweet data
    # run through flair models
    # output json file
    # FIN @ location of csv file
    # FOUT @ location for json file to be saved

    print("Reading in data.")

    df = pd.read_csv(FIN)

    count = 0  # global counting variable

    # filter dataframe for only USA tweets
    df = df[df['place_country_code'] == 'US']

    # load tagger
    pos_tagger = SequenceTagger.load('pos')

    print('Model has been loaded from flair.')

    ##########################
    # DEFINING FUNCTIONS

    def get_pos(sentence):
        # funtion to return all pos in a list
        # sentence @ pass in class Sentence from flair

        pos_tagger.predict(sentence)
        # tuple of (token, pos tag)
        pos = [(str(pos['text']), str(pos['labels'][0]).split()[0]) for pos in
               sentence.to_dict(tag_type='pos')['entities']]
        return pos

    def run_stack(date, place, text):
        # function to run whole stack and return a tuple
        # date @ pass in date to be put in json
        # place @ pass in place to be put in json
        # text @ text in date to be put in json and ran through flair

        # change to flair class, predict pos
        sentence = Sentence(text)
        pos = get_pos(sentence)

        if len(pos) is 0:
            pos = None

        global count
        count = count + 1

        if count % 1000 == 0:
            print("Completed {0} tweets.".format(count))

        return {"created_at": date, "place": place, "text": text, "pos": pos}

    def dump_tweet(W_FILENAME, TWEET):
        ## function to dump a single tweet
        # W_FILENAME @ pass in write filename, and tweet to write
        # TWEET @ function will append tweet to end of file

        with open(W_FILENAME, 'a') as fout:
            fout.write(json.dumps(TWEET))  # write tweet as string
            fout.write('\n')  # write new line at end

            # closing file
            fout.close()

    ##########################
    # RUNNING SCRIPT

    for row in (df[['created_at', 'place_full_name', 'text']].iterrows()):
        tweet = run_stack(row[1]['created_at'], row[1]['place_full_name'], row[1]['text'])
        dump_tweet(FOUT, tweet)

flair_pos(FIN, FOUT)

