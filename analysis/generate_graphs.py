import os
import json
import math
import pandas as pd
import wordcloud as wc
import matplotlib.pyplot as plt

############################
# HYPERPARAMETERS ##########
FIN = '2_flair_scripts/flair/flair_joined_tweets.json'
FOUT = 'analysis/viz/'  # folder location to create and save files in
############################


def clean_line(LINE):
    '''Function used to take line from json file, and clean it

    Parameters
    ----------
    LINE: pass in line from json file to be processed
    '''

    LINE = json.loads(LINE.rstrip())  # strip newline from end
    json.dumps(LINE)  # get in json format

    return LINE


def get_nested_string(data):
    # function returns a string of all nested words
    word_list = [words.lower()
                 for nest in data
                 if nest is not None
                 for words in nest]

    string = " ".join(word_list)

    return string


def get_string(data):
    # function returns a string of non nested words
    word_list = [word.lower()
                 for word in data
                 if word is not None
                 ]

    string = " ".join(word_list)

    return string


def get_pos_string(data, POS):
    word_list = [word.lower()
                 for pos_list in data
                 for (word, tag) in pos_list
                 if POS in tag
                 ]

    string = " ".join(word_list)

    return string


def count_nest_words(data):
    word_list = [words.lower()
                 for nest in data
                 if nest is not None
                 for words in nest
                 ]

    words_dict = {}

    for word in word_list:
        if word not in words_dict.keys():
            words_dict[word] = 1
        else:
            words_dict[word] = words_dict[word] + 1

    words_dict = {word: count for word, count in sorted(
        words_dict.items(), key=lambda item: item[1], reverse=True)}

    return words_dict


def dump_words(dict, FOUT):
    with open(FOUT, 'a') as fout:
        for word in dict:
            try:
                fout.write(str(word) + " " + str(dict[word]))
                fout.write('\n')
            except:
                pass

        fout.close()


def create_wordcloud(STRING, FOUT):
    # function creates a wordcloud and saves it to FOUT
    wordcloud = wc.WordCloud(
        stopwords=set(wc.STOPWORDS),
        width=800, height=800,
        background_color="black",
        min_font_size=10
    ).generate(STRING)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(FOUT)

########################
# LOADING DATA


print('Getting data')

with open(FIN) as fin:

    data = [clean_line(line) for line in fin]  # make list of dictionaries

    df = pd.DataFrame(data)  # dump list of dictionaries to df

    fin.close()

####################################################
# GENERATING WORDCLOUDS AND TEXT FILES

print('Creating folder.')

try:
    os.mkdir(FOUT)
except:
    pass

print('Generating wordclouds.')

try:
    os.mkdir(FOUT + 'text/')
except:
    pass

# getting wordcloud for all text
all_tweet = get_string(df['text'])
create_wordcloud(all_tweet, FOUT + 'text/all_wordcloud.png')

print('All text wordcloud created.')
######

# getting wordcloud for positive sentiment text
pos_tweet = get_string(df[df['sentiment'] == 'POSITIVE']['text'])
create_wordcloud(pos_tweet, FOUT + 'text/positive_wordcloud.png')

######

# getting wordcloud for negative sentiment text
neg_tweet = get_string(df[df['sentiment'] == 'NEGATIVE']['text'])
create_wordcloud(neg_tweet, FOUT + 'text/negative_wordcloud.png')

print('Sentiment wordclouds created.')
######

try:
    os.mkdir(FOUT + 'ner/')
except:
    pass

# getting wordcloud for named entity recognition
ner_string = get_nested_string(df['ner'])
create_wordcloud(ner_string, FOUT + 'ner/ner_all_wordcloud.png')
# getting count of named entity recognition
ner_dict = count_nest_words(df['ner'])
dump_words(ner_dict, FOUT + 'ner/ner_all_count.txt')

print('All ner wordcloud and count list created.')
######

# getting wordcloud for positive sentiment NER
pos_ner_string = get_nested_string(df[df['sentiment'] == 'POSITIVE']['ner'])
create_wordcloud(pos_ner_string, FOUT + 'ner/ner_positive_wordcloud.png')
# getting count of named entity recognition
pos_ner_dict = count_nest_words(df[df['sentiment'] == 'POSITIVE']['ner'])
dump_words(pos_ner_dict, FOUT + 'ner/ner_positive_count.txt')

######

# getting wordcloud for negative sentiment NER
neg_ner_string = get_nested_string(df[df['sentiment'] == 'NEGATIVE']['ner'])
create_wordcloud(neg_ner_string, FOUT + 'ner/ner_negative_wordcloud.png')
# getting count of named entity recognition
neg_ner_dict = count_nest_words(df[df['sentiment'] == 'NEGATIVE']['ner'])
dump_words(neg_ner_dict, FOUT + 'ner/ner_negative_count.txt')

print('NER sentiment wordclouds and counts created.')
######

try:
    os.mkdir(FOUT + 'pos/')
except:
    pass

# getting wordclous for verbs only
all_verb_string = get_pos_string(df['pos'], 'V')
create_wordcloud(all_verb_string, FOUT + 'pos/verb_all_wordcloud.png')

######

# getting wordclous for positive sentiment verbs only
pos_verb_string = get_pos_string(df[df['sentiment'] == 'POSITIVE']['pos'], 'V')
create_wordcloud(pos_verb_string, FOUT + 'pos/verb_positive_wordcloud.png')

######

# getting wordclous for negative sentiment verbs only
neg_verb_string = get_pos_string(df[df['sentiment'] == 'NEGATIVE']['pos'], 'V')
create_wordcloud(neg_verb_string, FOUT + 'pos/verb_negative_wordcloud.png')

print('All verb wordclouds created.')
######
