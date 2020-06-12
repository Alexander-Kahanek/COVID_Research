import pandas as pd
import json
from flair.data import Sentence
from flair.models import TextClassifier
from flair.models import SequenceTagger

##########################
# HYPERPARAMETERS ########
FIN = "tweets.csv"
FOUT = "nlp_tweets.json"
##########################

print("Reading in data.")

df = pd.read_csv(FIN)

count = 0

# filter dataframe for only USA tweets
df = df[df['place_country_code'] == 'US']

# load taggers
pos_tagger = SequenceTagger.load('pos')
ner_tagger = SequenceTagger.load('ner')
# load classifier
classifier = TextClassifier.load('sentiment')

def get_sentiment(sentence):
    # function to return sentiment string
    classifier.predict(sentence)
    # string of POSITIVE / NEGATIVE
    return sentence.to_dict()['labels'][0]['value']

def get_pos(sentence):
    # funtion to return all pos in a list
    pos_tagger.predict(sentence)
    # tuple of (token, pos tag)
    pos = [(str(pos['text']), str(pos['labels'][0]).split()[0]) for pos in sentence.to_dict(tag_type='pos')['entities']]
    return pos

def get_ner(sentence):
    # function to return all named entity recognitions in a list
    ner_tagger.predict(sentence)
    ner = [str(ner['text']) for ner in sentence.to_dict(tag_type='ner')['entities']]
    return ner

def run_stack(text):
    # function to run whole stack and return a tuple
    sentence = Sentence(text)

    sent = get_sentiment(sentence)
    ner = get_ner(sentence)
    pos = get_pos(sentence)

    if len(pos) is 0:
        pos = None

    if len(ner) is 0:
        ner = None

    global count
    count = count + 1

    if count % 1000 == 0:
        print("Completed {0} tweets.".format(count))

    return {"text":text, "sent":sent, "ner":ner, "pos":pos}

def dump_tweet(W_FILENAME, TWEET):
    ## function to dump a single tweet
    # W_FILENAME @ pass in write filename, and tweet to write
    # TWEET @ function will append tweet to end of file
    with open(W_FILENAME, 'a') as fout:
        fout.write(json.dumps(TWEET)) # write tweet as string
        fout.write('\n') # write new line at end

        # closing file
        fout.close()

for text in df['text']:

    tweet = run_stack(text)
    dump_tweet(FOUT, tweet)