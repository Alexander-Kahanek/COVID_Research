import gzip
import json
import os

##############################
# CHANGE THESE SETTING #######
DIRECTORY = 'raw/' # directory to grab files from
NEW_FOLDER = 'filtered/' # directory to create for cleaned json file/s/
CLEANED_FN = 'cleaned.json' # filename for filtered out tweets
COMPLETE_FILE = 'completed.txt' # filename to store list of completed files in
ERROR_FILE = 'error.txt' # filename to store list of error'd files in
##############################

def run_filter(RAW, CLEANED, CLEAN_FN, COMP_FN, ERROR_FN):
    ## function used to call full filter script
    # RAW @ pass in filename for RAW folder
    # CLEANED @ pass in filename created for cleaned file directory
    # CLEAN_FN @ pass in filename to store filtered tweets
    # COMP_FN @ pass in filename for list of completed files
    # ERROR_FN @ pass in filename for list of error files

    #############################
    # FUNCTIONS TO DEFINE

    def keep_tw(TWEET):
        ## function to check tweet qualifications to keep
        # TWEET @ pass in tweet to check
        if TWEET['geo'] != None:
            return True
        elif TWEET['coordinates'] != None:
            return True
        elif TWEET['place'] != None:
            return True

        return False

    def dump_tweet(W_FILENAME, TWEET):
        ## function to dump a single tweet
        # W_FILENAME @ pass in write filename, and tweet to write
        # TWEET @ function will append tweet to end of file
        with open(W_FILENAME, 'a') as fout:
            fout.write(json.dumps(TWEET))  # write tweet as string
            fout.write('\n')  # write new line at end

            # closing file
            fout.close()

    def dump_filename(FILE, FILENAME):
        ## function to dump a filename to a txt file
        # FILE @ pass in file to append
        # FILENAME @ pass in filename to add to file
        with open(FILE, 'a') as fout:
            fout.write(FILENAME)  # write filename to txt
            fout.write('\n')  # write newline at end

            # closing file
            fout.close()

    def check_fn(FILE, FILENAME):
        ## function to check if a file has already been completed
        # FILE @ pass in file to check
        # FILENAME @ pass in filename to check
        # returns True if filename is contained in file
        # returns False if filename is not contained in file
        try:
            with open(FILE, 'r') as fin:
                for line in fin:
                    if line.rstrip() == FILENAME:
                        # file is already filtered
                        fin.close()
                        return True
                fin.close()
        except:
            pass
        # file has not been filtered
        return False

    def fix_usr_vals(DIRECTORY, FILENAME=None):
        ## function used to check user set variables
        # DIRECTORY @ pass in directory to be checked
        # FILENAME @ pass in filename to be checked

        if DIRECTORY[-1] != '/':
            DIRECTORY = DIRECTORY + '/'

        if FILENAME == None:  # function done
            return DIRECTORY

        if FILENAME[0] == '/':
            return DIRECTORY + FILENAME[1:]
        else:
            return DIRECTORY + FILENAME

    ###############################################
    # SCRIPT STARTS

    # fixing user set values for ending or beginning '/'
    RAW = fix_usr_vals(RAW)
    CLEANED = fix_usr_vals(CLEANED)
    COMP_FN = fix_usr_vals(CLEANED, COMP_FN)
    ERROR_FN = fix_usr_vals(CLEANED, ERROR_FN)
    W_FILENAME = fix_usr_vals(CLEANED, CLEAN_FN)

    tot_files = len(os.listdir(RAW)) # total files to be filtered through
    cmp_files = 0  # counter for number of completed files
    tot_tweets = 0  # counter for total tweets

    # creating new directory
    try:
        os.makedirs(os.path.dirname(CLEANED))
    except:
        print('Directory {0} already exists, continuing with designated directory.'.format(CLEANED))
        pass

    print('Loading in all files from {0}'.format(RAW))

    for FILENAME in os.listdir(RAW):  # get filenames

        R_FILENAME = RAW + FILENAME  # add directory to filename

        if not check_fn(COMP_FN, R_FILENAME):
            # file has been filtered already

            try:

                with gzip.open(R_FILENAME, 'r') as fin:  # decompressing
                    data = [json.loads(line) for line in fin]  # loading in data

                # loop to search for tweets by qualifier
                for tweet in data:
                    if keep_tw(tweet) == True:
                        dump_tweet(W_FILENAME, tweet) # append tweet to file
                        tot_tweets = tot_tweets + 1

                fin.close()

                # file successfully filtered
                dump_filename(COMP_FN, R_FILENAME) # dump filename to text file
                cmp_files = cmp_files + 1

            except:  # error with loading file

                try:
                    fin.close()
                except:
                    pass

                print('\nFile could not be loaded. Filename is:\n**********\n{0}\n**********\n'.format(R_FILENAME))
                print('Closing current file and starting next file in line.')

                # error with file, dump to txt file for storage
                dump_filename(ERROR_FN, R_FILENAME)
                pass

            if (cmp_files % 10 == 0) & (cmp_files != 0):  # print update
                print('\nCompleted {0}/{1} files.'.format(cmp_files, tot_files))
                print('There are {0} tweets found with geo locations so far.'.format(tot_tweets))
    print('Found a total of {0} tweets.'.format(tot_tweets))
    print('Successfully opened {0}/{1} files from {2}'.format(cmp_files, tot_files, RAW))

run_filter(DIRECTORY, NEW_FOLDER, CLEANED_FN, COMPLETE_FILE, ERROR_FILE)