import pandas as pd
import preprocessor as p  # "pip3 install tweet-preprocessor"
import re

##########################
# HYPERPARAMETERS ########
FIN = "2_flair_scripts/filtered/tweets.csv"
FOUT = "2_flair_scripts/filtered/preprocessed_tweets.csv"
##########################


def preprocess_4_flair(FIN, FOUT):
    '''Function takes a csv from outputted by the json_2_csv_script.py,
    will add column for mentions, hashtags, and text cleaned of special characters.

    Parameters
    ----------
    FIN : location of file to be used
    FOUT : location to save new file to

    Returns
    -------
    Nothing
    '''

    ################################
    # DEFINING FUNCTIONS

    def clean_text(TEXT):
        '''Function cleans text of hashtags, mentions, hyperlinks,
        special characters, and stemms words

        Parameters
        ----------
        TEXT : a string to be cleaned

        Returns
        -------
        tweet-preprocessor cleaned, -(hashtags, mentions, hyperlinks),
        special characcters removed.
        '''
        # cleans out hashtags, mentions, hyperlinks
        cleaned_text = p.clean(TEXT)
        # lowered, stripped of newlines, clear special characters, except _
        cleaned_text = re.sub('\W+', ' ', cleaned_text.strip().lower())

        if len(cleaned_text) == 0:
            # print(cleaned_text)
            return " "

        return cleaned_text

    #############

    def clean_tag(MENTION):
        '''Function used to clean a tag.
        REMOVES: newlines, all special char but '_', lowercases.

        Parameters
        ----------
        MENTION : string that contains '@'

        Returns
        -------
        stripped of newlines, lowercased, removed all
        special characters except '_' (underscore).
        '''

        # lowered, stripped of newlines, clear special characters, except _
        MENTION = re.sub('\W+', '', MENTION.strip().lower())

        return MENTION

    ###################

    def get_mentions(TEXT):
        '''Function searches through text for tweet mentions.

        Parameters
        ----------
        TEXT : a string to be searched and split.

        Returns
        -------
        A list of strings, containing the @ mentions.

        '''
        if '@' in TEXT:
            split_text = TEXT.split(" ")

            mentioned_words = [clean_tag(text)
                               for text in split_text
                               if '@' in text and len(text) > 1]

            if len(mentioned_words) == 0:
                return None

        else:
            return None

        return mentioned_words

    #################

    def get_hashtags(TEXT):
        '''Function finds hashtags to be cleaned.

        Parameters
        ----------
        TEXT : a string to be searched and split.

        Returns
        -------
        A list of strings, containing # hashtags.
        '''

        if '#' in TEXT:
            split_text = TEXT.split(" ")

            hashtagged_words = [clean_tag(text)
                                for text in split_text
                                if '#' in text and len(text) > 1]

            if len(hashtagged_words) == 0:
                return None

        else:
            return None

        return hashtagged_words

    ############################################
    # SCRIPT STARTS

    print('Reading in data from {0}'.format(FIN))

    df = pd.read_csv(FIN)

    print('Data has been loaded.')

    # cleaning tweet text
    df['clean_text'] = [clean_text(text)
                        for text in df['text']]

    print('Text has been cleaned. 1/3 complete')

    # getting mentions from text
    df['mentions'] = [get_mentions(text)
                      for text in df['text']]

    print('Mentions have been found and stored. 2/3 complete')

    # getting hashtags from text
    df['hashtags'] = [get_hashtags(text)
                      for text in df['text']]

    print('Hashtags have been found and stored. 3/3 complete')
    print('Saving data to {0}'.format(FOUT))

    df.to_csv(FOUT, index=False)

    print('Data was stored in location. Script is finished.')


preprocess_4_flair(FIN, FOUT)
