import pandas as pd
import ast


def filter_pos(data, POS):
    '''
    takes the part-of-speech dataframe column, and filters
    the words for only the POS tag contained in POS.

    returns a list of words.
    '''

    # pos tags seem to follow these guidelines
    # https://cs.nyu.edu/grishman/jet/guide/PennPOS.html

    word_list = [word.lower()
                 for pos_list in data
                 if pos_list is not None
                 for (word, tag) in ast.literal_eval(pos_list)
                 if POS in tag
                 ]

    return word_list


def text_lister(data):
    '''
    takes a text dataframe column and returns a list of words
    '''

    word_list = [word
                 for text in data
                 if text != ""
                 for word in text.split(' ')
                 if len(word) > 2]

    return word_list


def count_words(words):
    '''
    takes a list of words, then counts, orders, and 
    returns a dataframe object
    '''

    words_dict = {}

    for word in words:
        if word not in words_dict.keys():
            words_dict[word] = 1
        else:
            words_dict[word] = words_dict[word] + 1

    words_dict = [{"word": word, "count": count}
                  for word, count in sorted(words_dict.items(), key=lambda item: item[1], reverse=True)
                  ]

    dataframe = pd.DataFrame(words_dict)

    return dataframe


def count_n_seperate(poslist, neglist, Nwords):
    '''
    takes positive and negative list, returns aligned dataframe
    '''

    # count lists
    posdf = count_words(poslist)
    negdf = count_words(neglist)

    # get counts
    negdf['count'] = negdf['count'] * -1
    df = posdf.merge(negdf, on='word')
    df['sum'] = df['count_x'] + (df['count_y'] * -1)
    df.columns = ['word', 'poscount', 'negcount', 'sum']
    dataframe = verbdf.nlargest(Nwords, 'sum')

    return dataframe


def search_phrases(data, phraselist):
    '''
    takes a dataframe object, and searches text for phrases and 
    returns a dataframe with 'is.phrase' col == [0,1]
    '''

    for phrase in phraselist:
        is_phrase = [1 if phrase in text else 0
                     for text in data['ogtext']]

        phrase = ".".join(phrase.split(' '))

        data[f'in.{phrase}'] = is_phrase

    return data


def ntweet_prop_dfs(data, c1, c2, pivot='ogtext'):
    '''
    takes data and two columns that will be grouped by, 
    ie, c1 = date, c2 = proportion.

    returns two dataframes for 
    number of tweets, proportion of c2, difference of c2 by c1
    '''
    # getting first dataframe ---- number of tweets
    # getting counts for c1 -> c2
    ntweetdf = data.groupby([c1, c2]).count()[pivot].reset_index()
    # renaming
    ntweetdf.columns = [c1, c2, 'num_of_tweets']

    # getting second dataframe ----- proportion
    # getting sum of hour -> sentiment
    sumc1 = ntweetdf.groupby([c1, c2]).agg({'num_of_tweets': 'sum'})
    # getting sum of hour
    sum = ntweetdf.groupby(c1).agg({'num_of_tweets': 'sum'})
    # making proportion
    propdf = sumc1.div(sum, level=c1) * 100

    # Sfinding difference of proportion for second dataframe
    propdf['diffs'] = propdf.groupby(
        [c2])['num_of_tweets'].transform(lambda x: x.diff())
    propdf = propdf.reset_index()
    # fill NaN value
    propdf['diffs'] = propdf['diffs'].fillna(0)

    propdf.columns = [c1, c2, 'proportion', 'difference']

    return ntweetdf, propdf


# raw = pd.read_csv('flair_joined_tweets.csv')

# # changing na to None
# raw = raw.fillna('None')

# # only 4 samples that have no sentiment
# raw = raw[raw['sentiment'] != 'None']

# # changing date to more readable format
# raw['created_at'] = pd.to_datetime(raw['created_at'])

# # getting seperated date and time columns
# raw['date'] = raw['created_at'].dt.date
# raw['time'] = raw['created_at'].dt.time
# raw['hour'] = raw['created_at'].dt.hour

# ntweetdf, propdf = ntweet_prop_dfs(raw, 'date', 'sentiment')

# print(ntweetdf)

# # adds columns for phrases
# df = search_phrases(raw, ['mask', 'social distancing'])
# print(df['in.social.distancing'].value_counts())

# for text in df[df['in.mask'] == 1]['ogtext'].head():
#     print(text)

# # count words in dataframe
# df = text_lister(raw['cleantext'])
# df = count_words(df)
# print(df.head(50))

# # search for wors by pos tags
# poslist = filter_pos(raw[raw['sentiment'] == 'POSITIVE']['pos'], 'VBD')  # vbn
# neglist = filter_pos(raw[raw['sentiment'] == 'NEGATIVE']['pos'], 'VBD')
# posdf = count_words(poslist)
# negdf = count_words(neglist)
# print(posdf.head(25))
# print(negdf.head(25))

# # unique POS tags list
# tags = [tag
#         for pos_list in raw['pos']
#         if pos_list is not None
#         for (word, tag) in ast.literal_eval(pos_list)
#         ]
# print(set(tags))
