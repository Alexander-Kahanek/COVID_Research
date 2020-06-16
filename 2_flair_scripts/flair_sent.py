import os
import pandas as pd
import json
from flair.data import Sentence
from flair.models import TextClassifier

##########################
# HYPERPARAMETERS ########
FIN = "2_flair_scripts/filtered/tweets.csv"
FOUT = "2_flair_scripts/flair"
##########################

count = 0  # global counting variable


def flair_sentiment(FIN, FOUT):
    """Function used to take csv tweet data run through flair models output json file 

    Parameters
    ----------
    FIN: filepath for csv

    FOUT: filepath to store new json into
    """

    print("Reading in data.")

    df = pd.read_csv(FIN)

    count = 0  # global counting variable

    # filter dataframe for only USA tweets
    df = df[df['place_country_code'] == 'US']

    # load classifier
    classifier = TextClassifier.load('sentiment')

    print('Model has been loaded from flair.')

    ##########################
    # DEFINING FUNCTIONS

    def get_sentiment(sentence):
        '''Function to return sentiment string

        Parameters
        ----------
        sentence : pass in class Sentence from flair

        Returns
        -------
        sentiment as string
        '''

        classifier.predict(sentence)
        # string of POSITIVE / NEGATIVE
        return sentence.to_dict()['labels'][0]['value']

    def run_stack(date, place, text):
        '''Function to run flair stack

        Parameters
        ----------
        date : pass in date to be put in json

        place : pass in place to be put in json

        text : pass in text to be put in json and ran through flair

        Returns
        -------
        dictionarty object
        '''

        # change to flair class, predict sentiment
        sentence = Sentence(text)
        sent = get_sentiment(sentence)

        global count
        count = count + 1

        if count % 1000 == 0:
            print("Completed {0} tweets.".format(count))

        return {"created_at": date, "place": place, "text": text, "sent": sent}

    def dump_tweet(W_FILENAME, TWEET):
        '''Function to dump a single tweet

        Parameters
        ----------
        W_FILENAME : pass in write filename, and tweet to write

        TWEET : function will append tweet to end of file
        '''

        with open(W_FILENAME, 'a') as fout:
            fout.write(json.dumps(TWEET))  # write tweet as string
            fout.write('\n')  # write new line at end

            # closing file
            fout.close()

    ##########################
    # RUNNING SCRIPT

    try:
        os.mkdir(FOUT)
    except:
        pass

    print('Running Script.')

    for row in (df[['created_at', 'place_full_name', 'text']].iterrows()):
        tweet = run_stack(row[1]['created_at'],
                          row[1]['place_full_name'],
                          row[1]['text']
                          )
        dump_tweet(FOUT + '/sentiment_tweets.json', tweet)

    print('Script has finished.')


flair_sentiment(FIN, FOUT)
