import os
import pandas as pd
import json
from flair.data import Sentence
from flair.models import TextClassifier


def flair_sentiment(FIN="filteredtweets/preprocessed_tweets.csv", FOUT="flair"):
    """Function used to take csv tweet data run through flair models output json file 

    Parameters
    ----------
    FIN: filepath for csv

    FOUT: filepath to store new json into
    """

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

    def run_stack(count, date, place, language, mentions, hashtags, text):
        '''Function to run flair stack

        Parameters
        ----------
        date : pass in date to be put in json

        place : pass in place to be put in json

        language : pass in language tag to be put in json

        mentions : pass in list of mentions

        hashtags : pass in list of hashtags

        text : pass in text to be put in json and ran through flair

        Returns
        -------
        dictionarty object, counter
        '''

        try:
            # change to flair class, predict sentiment
            sentence = Sentence(text)
            sent = get_sentiment(sentence)
        except:
            text = None
            sent = None

        try:
            count = count + 1

            if count % 1000 == 0:
                print("Completed {0} tweets.".format(count))
        except:
            pass

        return {"created_at": date,
                "place": place,
                "language": language,
                "mentions": mentions,
                "hashtags": hashtags,
                "text": text,
                "sent": sent}, count

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

    def main(FIN, FOUT):

        print("Reading in data.")

        df = pd.read_csv(FIN)

        count = 0  # global count

        # filter dataframe for only USA tweets
        df = df[df['place_country_code'] == 'US'].fillna('None')

        df = df[df['language'] == 'en']

        # load classifier
        classifier = TextClassifier.load('sentiment')

        print('Model has been loaded from flair.')

        try:
            os.mkdir(FOUT)
        except:
            pass

        print('Running Script.')

        for row in (df[['created_at', 'place_full_name', 'language', 'mentions', 'hashtags', 'clean_text']].iterrows()):
            tweet, count = run_stack(count,
                                     row[1]['created_at'],
                                     row[1]['place_full_name'],
                                     row[1]['language'],
                                     row[1]['mentions'],
                                     row[1]['hashtags'],
                                     row[1]['clean_text']
                                     )
            dump_tweet(FOUT + '/sentiment_tweets.json', tweet)

        print('Script has finished.')

    main(FIN, FOUT)


# ##### EXAMPLE ############
# # HYPERPARAMETERS ########
# FIN = "filteredtweets/preprocessed_tweets.csv"
# FOUT = "flair"
# ##########################

# flair_sentiment(FIN, FOUT)
