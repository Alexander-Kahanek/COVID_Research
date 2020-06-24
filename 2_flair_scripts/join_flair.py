import json
import pandas as pd
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm as spaCy_lemm  # "python -m spacy download en"

##########################
# HYPERPARAMETERS ########
POS_FIN = '2_flair_scripts/flair/pos_tweets.json'
NER_FIN = '2_flair_scripts/flair/ner_tweets.json'
SENT_FIN = '2_flair_scripts/flair/sentiment_tweets.json'
FOUT = '2_flair_scripts/flair/'
##########################


def join_flair_2_json(POS_FIN, NER_FIN, SENT_FIN, FOUT):
    '''Function takes 3 json files from the flair algorithm,
    and combines them into one json file and one csv file.

    Paramters
    ---------
    POS_FIN : file location for pos json

    NER_FIN : file location for ner json

    SENT_FIN : file location for sentiment json

    FOUT : file location to store new json and csv, NOT NAME OF FILE
    '''

    ##########################
    # DEFINING FUNCTIONS

    def clean_line(LINE):
        '''Function used to take line from json file, and clean it

        Parameters
        ----------
        LINE : line from json file to be processed
        '''

        LINE = json.loads(LINE.rstrip())  # strip newline from end
        json.dumps(LINE)  # get in json format

        return LINE

    def remove_stopwords(STRING):
        '''Function is used to remove stopwords from a string.

        Parameters
        ----------
        STRING : a string to be filtered
        '''

        # Load English tokenizer, tagger, parser, NER and word vectors
        spacy = English()

        #  "nlp" Object is used to create documents with linguistic annotations.
        spacy_string = spacy(STRING)

        # Create list of word tokens
        token_list = [token.text
                      for token in spacy_string]

        # Create list of word tokens after removing stopwords
        filtered_sentence = [word
                             for word in token_list
                             if spacy.vocab[word].is_stop is False]

        # join and return string
        return " ".join(filtered_sentence)

    def stem_words(STRING):
        '''Function is used to stem words in a string.

        Parameters
        ----------
        STRING : a string to be modified
        '''

        # load spacy english lemma model
        spacy_model = spaCy_lemm.load()

        # create model object
        spacy_string = spacy_model(STRING)

        # create list of lemma
        lemma_list = [token.lemma_
                      for token in spacy_string]

        # join and return string
        return " ".join(lemma_list)

    def stop_n_stem(STRING):
        '''Function will take a string and remove stopwords,
        then function will stem all words.

        Parameters
        ----------
        STRING : a string to be modified

        Returns
        -------
        A modified string type
        '''

        # use spaCy to remove stopwords and stem words
        STRING = remove_stopwords(STRING)
        STRING = stem_words(STRING)

        return STRING

    def dump_dictionary(DICTIONARY, FOUT):
        '''Funtion takes dictionary and appends it to file

        Parameters
        ----------
        DICTIONARY : dictionary object to be appended

        FOUT : file and name location to append to
        '''

        with open(FOUT, 'a') as fout:
            fout.write(json.dumps(DICTIONARY))
            fout.write('\n')
            fout.close()

    def join_lists(counter, pos_list, ner_list, sent_list):
        '''Function joins tweets from 3 lists into one single list

        Parameters
        ----------
        counter : counter for lists to keep track

        pos_list : list of dictionary objects, part of speech

        ner_list : list of dictionary objects, named entity recognition

        sent_list : list of dictionary objects, sentiment

        Returns
        -------
        dictionary object
        '''

        # change to strings for text that is NoneType
        pos_text = str(pos_list[counter]['text'])
        ner_text = str(ner_list[counter]['text'])
        sent_text = str(sent_list[counter]['text'])

        # strip newlines from text
        pos_text = pos_text.strip()
        ner_text = ner_text.strip()
        sent_text = sent_text.strip()

        if counter % 1000 == 0:
            print('Completed joining {0} tweets'.format(counter))

        if pos_text is not "":
            pos_text = stop_n_stem(pos_text)

        new_dictionary = {"created_at": pos_list[counter]['created_at'],
                          "place": pos_list[counter]['place'],
                          "text": pos_text,
                          "mentions": pos_list[counter]['mentions'],
                          "hashtags": pos_list[counter]['hashtags'],
                          "pos": pos_list[counter]['pos'],
                          "ner": ner_list[counter]['ner'],
                          "sentiment": sent_list[counter]['sent']}

        return new_dictionary

    ##########################################
    # SCRIPT STARTS

    print('Script is starting...')

    # open and store all 3 files in lists
    with open(POS_FIN) as pos_fin:
        pos_dict_list = [clean_line(LINE) for LINE in pos_fin]
        pos_fin.close()

    with open(NER_FIN) as ner_fin:
        ner_dict_list = [clean_line(LINE) for LINE in ner_fin]
        ner_fin.close()

    with open(SENT_FIN) as sent_fin:
        sent_dict_list = [clean_line(LINE) for LINE in sent_fin]
        sent_fin.close()

    print('Original json files are loaded.')

    for line_count in range(len(pos_dict_list)):
        # join all 3 dictionaries into 1 dictionary
        new_dict = join_lists(line_count,
                              pos_dict_list,
                              ner_dict_list,
                              sent_dict_list)

        # dump dictionary to file
        dump_dictionary(new_dict, FOUT + 'flair_joined_tweets.json')

    print('json file has been created and dumped to {0}'.format(
        FOUT + 'flair_joined_tweets.json'))

    # reading in joined json file that was created
    with open(FOUT + 'flair_joined_tweets.json') as joined_fin:
        joined_dictionaries = [clean_line(LINE) for LINE in joined_fin]
        joined_fin.close()

    # creating DataFrame from json file
    joined_df = pd.DataFrame(joined_dictionaries)
    joined_df.to_csv(FOUT + 'flair_joined_tweets.csv', index=False)

    print('csv file has been created and was dumped to {0}'.format(
        FOUT + 'flair_joined_tweets.csv'))


join_flair_2_json(POS_FIN, NER_FIN, SENT_FIN, FOUT)
