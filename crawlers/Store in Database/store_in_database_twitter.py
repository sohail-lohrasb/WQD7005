import pymysql
import pymysql.cursors
import os
import re
import pandas as pd

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# create a dictionary that maps company full names to company symbols
with open('data/company_fullnames.txt') as f:
    company_fullnames = [x.strip() for x in f.readlines()]
with open('data/company_symbols.txt') as f:
    company_symbols = [x.strip() for x in f.readlines()]
fullname_to_symbol = {}
for i in range(len(company_fullnames)):
    fn = re.sub(r'(.*:\s*)|(\s*\(.*\))|(\s*BERHAD)|(\s*BHD)', '', company_fullnames[i])
    fullname_to_symbol[fn] = company_symbols[i]


# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Asdlkj987!23',
                             db='data_mining_assignment',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

twitter_data = pd.read_csv('data/fullname_tweets.csv').reset_index(drop=True)

for i in range(twitter_data.shape[0]):
    tweet = twitter_data.iloc[i, :]
    company_fullname = tweet['company_fullname']
    company_symbol = fullname_to_symbol[company_fullname]
    tweet_text = tweet['tweet_text']
    tweet_text = re.sub(r'\n', '. ', tweet_text)
    favorite_count = int(tweet['favorite_count'])
    created_at = tweet['created_at']
    hashtags = tweet['hashtags']
    if pd.isna(hashtags):
        hashtags = None   
    tweet_id = str(tweet['tweet_id'])
    lang = tweet['lang']
    urls = tweet['urls']
    if pd.isna(urls):
        urls = None
    user_followers = int(tweet['user_followers'])
    user_screen_name = tweet['user_screen_name']
    crawling_time = tweet['crawling_time']
    try:
        with connection.cursor() as cursor:
            # Create new records
            sql = "INSERT INTO `Tweets` (`CompanyFullname`, `CompanySymbol`, `TweetText`, `FavoriteCount`,"\
                    " `CreatedAt`, `HashTags`, `TweetId`, `Language`, `Urls`, `UserFollowers`, `UserScreenName`,"\
                    " `CrawlingTime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,
                            (company_fullname, company_symbol, tweet_text, favorite_count, created_at, hashtags,
                             tweet_id, lang, urls, user_followers, user_screen_name, crawling_time))
        connection.commit()
    except BaseException:
        print('Error while inserting a new entry into the database')
        print(BaseException)
connection.close()
