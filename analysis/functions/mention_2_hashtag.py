import pandas as pd
import ast


def get_mentions_hashtags(data, Nmentions, Nhashtags):
    '''Function returns N mentions-hashtage pairs, where neither
    mentions or hashtags can be None.

    Parameters
    ----------
    data : DataFrame object with 'mention' and 'hashtag' columns
    being a list of strings.

    Nmentions : number of top mentions to choose.

    Nhashtags : number of top hashtags to choose from the top mentions.

    '''

    ############################################
    # DEFINING FUNCTIONS

    def fix_list(tags):
        '''Function fixes tags so that they are lists

        Parameters
        ----------
        tags : the tags to be passed in
        '''

        if tags == "None":
            return ['None']
        else:
            try:
                tags = ast.literal_eval(tags)

                tags = [tag
                        for tag in tags
                        if tag != "" and tag is not None]

                return tags
            except:
                return tags

    def join_lists(mention_list, hashtag_list):
        '''Function joins mention list and hashtag list into
        a list of dictionary objects

        Parameters
        ----------
        mention_list : a list of all mentions for a given row

        hashtag_list : a list of all hashtags for a given row
        '''

        all_pairs = [{"mention": mention, "hashtag": hashtag, "count": 1}
                     for mention in mention_list
                     for hashtag in hashtag_list]

        return all_pairs

    def find_dataframe(data, index, Nhashtags, top_mentions, top_counts):
        '''Function gets the dataframe for a given mention

        Parameters
        ----------
        data : data should be formatted at ['mention', 'hashtag', 'count'],
        values should already be counted.

        index : index of loop from number of mentions

        Nhashtags : how many hashtags to keep

        top_mentions : list of top mentions

        top_counts : list of top counts that correspond to top mentions
        '''

        data = data[data['mention'] == top_mentions[index]]
        data = data[data['hashtag'] != 'None'].sort_values(
            'count', ascending=False)
        data = data[0:Nhashtags]
        data['proportion'] = data['count']/top_counts[index]

        return data.reset_index()

    def main(data, Nmentions, Nhashtags):

        ###########################################
        # SCRIPT STARTS HERE

        data = data.fillna('None')

        mentions = [fix_list(mentions)  # list of all mentions per row
                    for mentions in data['mentions']]

        hashtags = [fix_list(hashtags)  # list of all hashtags per row
                    for hashtags in data['hashtags']]

        # list of dictionary objects for each row
        paired_rows = [join_lists(mentions[index], hashtags[index])
                       for index in range(len(mentions))]

        # seperate out dictionaries
        all_dictionaries = [dictionary
                            for row in paired_rows
                            for dictionary in row]

        paired_df = pd.DataFrame(all_dictionaries)

        #############
        # getting top N mention data
        top_df = paired_df[paired_df['hashtag'] != 'None'].groupby(
            ['mention']).count().reset_index()

        top_df = top_df[
            top_df['mention'] != 'None'].sort_values('count', ascending=False)

        top_mentions = [mention
                        for mention in top_df[0:Nmentions]['mention']]

        top_counts = [count
                      for count in top_df[0:Nmentions]['count']]
        ############

        # getting top mention -> hashtag data
        mention_hashtag = paired_df.groupby(
            ['mention', 'hashtag']).count().reset_index()

        # seperating out dataframes into a list of individual DF objs
        df_list = [find_dataframe(mention_hashtag, index, Nhashtags, top_mentions, top_counts)
                   for index in range(Nmentions)]

        merged_data = pd.concat(df_list).reset_index().drop(
            columns=['level_0', 'index'])

        merged_data.columns = ['mention', 'hashtag', 'count', 'proportion']

        return merged_data

    return main(data, Nmentions, Nhashtags)
