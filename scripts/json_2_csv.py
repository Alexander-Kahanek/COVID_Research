import pandas as pd
import json


def join_json_to_csv(FIN='filteredtweets/filtered.json', FOUT='filteredtweets/allfilteredtweets.csv'):
    '''
    takes json file from decompress_and_filter.py and
    converts file into a csv for general analysis

    Parameters
    ----------
    FIN : file location of the filtered json file

    FOUT : file location and name for the filtered csv file
    '''

    #################################
    # FUNCTIONS TO DEFINE

    cnt_tweet = 0  # global variable for counting the number of lines that have been processed

    def get_cnt():
        # function to keep track of the number of tweets processed
        # do not pass anything in

        global cnt_tweet

        cnt_tweet = cnt_tweet + 1

        if cnt_tweet % 1000 == 0:
            print('Have completed {0} tweets'.format(cnt_tweet))

    def get_coordinates(LINE):
        # function used to get geo enabled coordinates
        # LINE @ pass in line to be processed

        try:
            data = LINE['coordinates']['coordinates']
            return data
        except:
            return None

    def get_place_coor(LINE):
        # function used to get place -> bounding_box data
        # LINE @ pass in line to be processed

        try:
            data = LINE['place']['bounding_box']['coordinates']
            return data
        except:
            # place is null
            return None

    def get_place_country(LINE):
        # function used to get place -> country data
        # LINE @ pass in line to be processed

        try:
            data = LINE['place']['country']
            return data
        except:
            # place is null
            return None

    def get_place_code(LINE):
        # function used to get place -> country code
        # LINE @ pass in line to be processed

        try:
            data = LINE['place']['country_code']
            return data
        except:
            # place is null
            return None

    def get_place_name(LINE):
        # function used to get place -> full_name
        # LINE @ pass in line to be processed

        try:
            data = LINE['place']['full_name']
            return data
        except:
            # place is null
            return None

    def get_place_type(LINE):
        # function used to get place -> place_type
        # LINE @ pass in line to be processed

        try:
            data = LINE['place']['place_type']
            return data
        except:
            # place is null
            return None

    def clean_line(LINE):
        # function used to take line from json file, and transfer it to a dictionary
        # LINE @ pass in line from json file to be processed

        LINE = json.loads(LINE.rstrip())  # strip newline from end
        json.dumps(LINE)  # get in json format

        # create dictionary with column names wanted
        # functions are used for attributes that could be null
        dict = {'created_at': LINE['created_at'],
                'user_id_str': LINE['user']['id_str'],
                'text': LINE['full_text'],
                'coordinates': get_coordinates(LINE),
                'place_coordinates': get_place_coor(LINE),
                'place_country': get_place_country(LINE),
                'place_country_code': get_place_code(LINE),
                'place_full_name': get_place_name(LINE),
                'place_type': get_place_type(LINE),
                'language': LINE['lang']}

        get_cnt()  # print function for tracker
        return dict

    def main():
        print('Grabbing data from {0}'.format(FIN))
    with open(FIN) as fin:

        data = [clean_line(line) for line in fin]  # make list of dictionaries

        df = pd.DataFrame(data)  # dump list of dictionaries to df

        print('Found {0} total tweets'.format(cnt_tweet))
        print('All tweets gathered, outputting to {0}'.format(FOUT))
        df.to_csv(FOUT, index=False)  # dump df to csv file

    main()

######## EXAMPLE #############
# SETTING TO CHANGE ##########
# fin = 'filtered/cleaned.json'  # file to get json data from
# fout = 'filtered/tweets.csv'  # file to output csv to
##############################

# join_json_to_csv(fin, fout)
