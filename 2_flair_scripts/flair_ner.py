import os
import pandas as pd
import json
from flair.data import Sentence
from flair.models import SequenceTagger

##########################
# HYPERPARAMETERS ########
FIN = "2_flair_scripts/filtered/tweets.csv"
FOUT = "2_flair_scripts/flair"
##########################

count = 0  # global counting variable

def flair_ner(FIN, FOUT):
    """ 
    function used to take csv tweet data run through flair models output json file 
    :param FIN: filepath for csv
    :param FOUT: filepath to store new json into
    :returns: nothing
    """
    # FIN @ location of csv file
    # FOUT @ location for json file to be saved

    print("Reading in data.")

    df = pd.read_csv(FIN)

    count = 0  # global counting variable

    # filter dataframe for only USA tweets
    df = df[df['place_country_code'] == 'US']

    # load taggers
    ner_tagger = SequenceTagger.load('ner')

    print('Model has been loaded from flair.')

    ##########################
    # DEFINING FUNCTIONS

    def get_ner(sentence):
        '''
        function to get named entity recognition with flair
        :param sentence: pass in class Sentence from flair
        :returns: ner in a list format [NER, ...]
        '''

        ner_tagger.predict(sentence)
        ner = [str(ner['text']) for ner in sentence.to_dict(tag_type='ner')['entities']]
        return ner

    def run_stack(date, place, text):
        '''
        function to run flair stack
        :param date: pass in date to be put in json
        :param place: pass in place to be put in json
        :param text: text in date to be put in json and ran through flair
        :returns: dictionarty object
        '''

        # change to flair class, predict ner
        sentence = Sentence(text)
        ner = get_ner(sentence)

        if len(ner) == 0:
            ner = None

        global count
        count = count + 1

        if count % 1000 == 0:
            print("Completed {0} tweets.".format(count))

        return {"created_at": date, "place": place, "text": text, "ner": ner}

    def dump_tweet(W_FILENAME, TWEET):
        '''
        function to dump a single tweet
        :param W_FILENAME: pass in write filename, and tweet to write
        :param TWEET: function will append tweet to end of file
        '''

        with open(W_FILENAME, 'a') as fout:
            fout.write(json.dumps(TWEET))  # write tweet as string
            fout.write('\n')  # write new line at end

            # closing file
            fout.close()

    ##########################
    # RUNNING SCRIPT

    os.mkdir(FOUT)

    print('Running Script.')

    for row in (df[['created_at', 'place_full_name', 'text']].iterrows()):
        tweet = run_stack(row[1]['created_at'], row[1]['place_full_name'], row[1]['text'])
        dump_tweet(FOUT + '/ner_tweets.json', tweet)

flair_ner(FIN, FOUT)