import json
import pandas as pd

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

        #######################################
        # clean text??????????????????????????????
        pos_text = pos_list[counter]['text'].rstrip()
        ner_text = ner_list[counter]['text'].rstrip()
        sent_text = sent_list[counter]['text'].rstrip()

        # ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        #print(pos_text, '/n', ner_text, '/n', sent_text, counter)

        if pos_text == ner_text and ner_text == sent_text:  # fffffffffffffffffffffffff
            # texts are the same, ie tweets are the same

            if counter % 1000 == 0:
                print('Completed joining {0} tweets'.format(counter))

            new_dictionary = {"created_at": pos_list[counter]['created_at'],
                              "place": pos_list[counter]['place'],
                              "text": pos_text,
                              "pos": pos_list[counter]['pos'],
                              "ner": ner_list[counter]['ner'],
                              "sentiment": sent_list[counter]['sent']}

            return new_dictionary
        else:
            # texts are not the same
            print('ERROR occured at tweet #{0}'.format(counter))
            print(pos_text, '/n', ner_text, '/n', sent_text, '/n', counter)
            new_dictionary = {"Error": counter}
            return new_dictionary

    def dump_dictonary(DICTIONARY, FOUT):
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

    # join all 3 dictionaries into 1 dictionary
    joined_dictionaries = [join_lists(line_count, pos_dict_list, ner_dict_list, sent_dict_list)
                           for line_count in range(len(pos_dict_list))]

    print('json files are all joined. Dumping files')

    # dump dictionary list to json and csv
    for dictionary in joined_dictionaries:
        dump_dictonary(dictionary, FOUT + 'flair_joined_tweets.json')

    print('json file has been created and dumped to {0}'.format(
        FOUT + 'flair_joined_tweets.json'))

    joined_df = pd.DataFrame(joined_dictionaries)
    joined_df.to_csv(FOUT + 'flair_joined_tweets.csv')

    print('csv file has been created and was dumped to {0}'.format(
        FOUT + 'flair_joined_tweets.csv'))


join_flair_2_json(POS_FIN, NER_FIN, SENT_FIN, FOUT)
