import os
import pandas as pd
import json
from flair.data import Sentence
from flair.models import SequenceTagger


def flair_pos(FIN="filteredtweets/preprocessed_tweets.csv", FOUT="flair"):
    '''Function used to take csv tweet data run through flair models output json file 

    Parameters
    ----------
    FIN : filepath for csv

    FOUT : filepath to store new json into
    '''

    ##########################
    # DEFINING FUNCTIONS

    def get_pos(sentence):
        '''Function to get part of speech with flair

        Parameters
        ----------
        sentence : pass in class Sentence from flair

        Returns
        -------
        pos in a list format [(word, tag), ...]
        '''

        pos_tagger.predict(sentence)
        # tuple of (token, pos tag)
        pos = [(str(pos['text']), str(pos['labels'][0]).split()[0]) for pos in
               sentence.to_dict(tag_type='pos')['entities']]
        return pos

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
            # change to flair class, predict pos
            sentence = Sentence(text)
            pos = get_pos(sentence)
        except:
            text = None
            pos = None

        if len(pos) == 0:
            pos = None

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
                "pos": pos}, count

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

        count = 0  # global counting variable

        # filter dataframe for only USA tweets and english
        df = df[df['place_country_code'] == 'US'].fillna('None')

        df = df[df['language'] == 'en']

        # load tagger
        pos_tagger = SequenceTagger.load('pos-fast')

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
            dump_tweet(FOUT + '/pos_tweets.json', tweet)

        print('Script has finished.')

    main(FIN, FOUT)


# #### EXAMPLE #############
# # HYPERPARAMETERS ########
# FIN = "filtered/preprocessed_tweets.csv"
# FOUT = "flair"
# ##########################

# flair_pos(FIN, FOUT)
