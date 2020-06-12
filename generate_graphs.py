import json
import pandas as pd
import wordcloud as wc
import matplotlib.pyplot as plt

############################
# HYPERPARAMETERS ##########
FIN = 'test.json'
############################


def clean_line(LINE):
    ## function used to take line from json file, and clean it
    # LINE @ pass in line from json file to be processed

    LINE = json.loads(LINE.rstrip()) # strip newline from end
    json.dumps(LINE) # get in json format

    return LINE

def get_nested_string(data):
    # function returns a string of all nested words
    word_list = [words.lower() for nest in data if nest is not None for words in nest]

    string = ""

    for word in word_list:
        string = string + " " + word
    
    return string

def get_string(data):
    # function returns a string of non nested words
    word_list = [word for word in data]

    string = ""

    for word in word_list:
        if word is not None:
            string = string + " " + word 

    return string

def get_pos_string(data, POS):
    word_list = [word for pos_list in data for (word,tag) in pos_list if POS in tag]
  
    string = ""

    for word in word_list:
        string = string + " " + word

    return string

def count_words(data):
    word_list = [words.lower() for nest in data if nest is not None for words in nest]
  
    words_dict = {}

    for word in word_list:
        if word not in words_dict.keys():
        words_dict[word] = 1
    else:
        words_dict[word] = words_dict[word] + 1

    words_dict = {word: count for word, count in sorted(words_dict.items(), key=lambda item: item[1], reverse= True)}

    return words_dict

def dump_words(dict, FOUT):
    with open(FOUT, 'a') as fout:
        for word in dict:
            fout.write(str(word) + " " + str(dict[word]))
            fout.write('\n')

            fout.close()

def create_wordcloud(STRING, FOUT):
    # function creates a wordcloud and saves it to FOUT
    wordcloud = wc.WordCloud(
    width = 800, height = 800,
    background_color = "black",
    min_font_size = 10
    ).generate(STRING)

    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.savefig(FOUT)

########################
# LOADING DATA

with open(FIN) as fin:

    data = [clean_line(line) for line in fin] # make list of dictionaries

    df = pd.DataFrame(data) # dump list of dictionaries to df

####################################################
# GENERATING WORDCLOUDS AND TEXT FILES

# getting wordcloud for all text
pos_tweet = get_string(df['text'])
create_wordcloud(pos_tweet, 'viz/text/all_wordcloud.png')

######

# getting wordcloud for positive sentiment text
pos_tweet = get_string(df[df['sent'] == 'POSITIVE']['text'])
create_wordcloud(pos_tweet, 'viz/text/positive_wordcloud.png')

######

# getting wordcloud for negative sentiment text
neg_tweet = get_string(df[df['sent'] == 'NEGATIVE']['text'])
create_wordcloud(neg_tweet, 'viz/text/negative_wordcloud.png')

######

# getting wordcloud for named entity recognition
ner_string = get_nested_string(df['ner'])
create_wordcloud(ner_string, 'viz/ner/ner_all_wordcloud.png')
# getting count of named entity recognition
ner_dict = count_words(df['ner'])
dump_words(ner_dict, 'viz/ner/ner_all_count.txt')

######

# getting wordcloud for positive sentiment NER
pos_ner_string = get_nested_string(df[df['sent'] == 'POSITIVE']['ner'])
create_wordcloud(pos_ner_string, 'viz/ner/ner_positive_wordcloud.png')
# getting count of named entity recognition
pos_ner_dict = count_words(df[df['sent'] == 'POSITIVE']['ner'])
dump_words(pos_ner_dict, 'viz/ner/ner_positive_count.txt')

######

# getting wordcloud for negative sentiment NER
neg_ner_string = get_nested_string(df[df['sent'] == 'NEGATIVE']['ner'])
create_wordcloud(neg_ner_string, 'viz/ner/ner_negative_wordcloud.png')
# getting count of named entity recognition
neg_ner_dict = count_words(df[df['sent'] == 'NEGATIVE']['ner'])
dump_words(pos_ner_dict, 'viz/ner/ner_negative_count.txt')

######

# getting wordclous for verbs only
all_verb_string = get_pos_string(df['pos'], 'V')
create_wordcloud(all_verb_string, 'viz/pos/verb_all_wordcloud.png')

######

# getting wordclous for positive sentiment verbs only
pos_verb_string = get_pos_string(df[df['sent'] == 'POSITIVE']['pos'], 'V')
create_wordcloud(pos_verb_string, 'viz/pos/verb_positive_wordcloud.png')

######

# getting wordclous for negative sentiment verbs only
ned_verb_string = get_pos_string(df[df['sent'] == 'NEGATIVE']['pos'], 'V')
create_wordcloud(ned_verb_string, 'viz/pos/verb_negative_wordcloud.png')

######