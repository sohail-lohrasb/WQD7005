import twitter
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import time
import re
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

api = twitter.Api(consumer_key='bg47VgnvB83qypdhR2d7w4bsP',
                  consumer_secret='LGOaENfzRsUEhuESTOVysDt6I7iKK6Lub4pu7eXxT748lSvlh0',
                  access_token_key='329665949-LTYBPi2PJFNQ9BbxwzECbeSSnlD8fxxb3ys8Afoi',
                  access_token_secret='5E4EK3xapVTQfCVMfQuug0cXyFDJJfgVeVvHBIvC3mPrF',
                  tweet_mode='extended')

if not (os.path.exists('symbol_tweets.csv')
        and os.path.exists('fullname_tweets.csv')):
    symbol_tweets_df = pd.DataFrame(columns=['company_symbol', 'tweet_text', 'favorite_count', 'created_at', 'hashtags',
                                             'tweet_id', 'lang', 'urls', 'user_followers', 'user_screen_name', 'crawling_time'])
    fullname_tweets_df = pd.DataFrame(columns=['company_fullname', 'tweet_text', 'favorite_count', 'created_at', 'hashtags',
                                               'tweet_id', 'lang', 'urls', 'user_followers', 'user_screen_name', 'crawling_time'])
else:
    symbol_tweets_df = pd.read_csv('symbol_tweets.csv', engine='python')
    fullname_tweets_df = pd.read_csv('fullname_tweets.csv')

company_symbols = []
with open("company_symbols.txt") as f:
    for line in f:
        company_symbols.append(line.strip())

company_fullnames = []
with open("company_fullnames.txt") as f:
    for line in f:
        company_fullnames.append(line.strip())

# search for tweets since 2 days before today until yesterday
# search_start = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
# search_end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
# sym missing (2019-03-10 -> 2019-03-11, )
# search_start = '2019-03-10' #first
# search_end = '2019-03-11'
search_start = '2019-03-16'
search_end = '2019-03-17'



if len(sys.argv) == 2:
    sym_or_fn = sys.argv[1]
else:
    sys.exit()


def crawl_tweets(sym_or_fn, df):
    """
    sym_or_fn should be equal to 'sym' to crawl tweets that contain company
    symbols or equal to 'fn' to crawl tweets that contain company full names
    """
    print('Crawling tweets containing company',
          'symbols' if sym_or_fn == 'sym' else 'full names',
          time.strftime('%H:%M'))
    if sym_or_fn == 'sym':
        company_labels = company_symbols
    else:
        company_labels = company_fullnames
        # Since company full formal names like 'AIRASIAC59: CW AIRASIA GROUP BERHAD (MACQ)'
        # for example will not be used usually in tweets, we will apply some
        # operations to them so the name above becomes 'CW AIRASIA GROUP'
        company_labels = [re.sub(r'(.*:\s*)|(\s*\(.*\))|(\s*BERHAD)|(\s*BHD)', '', com_fn)
                          for com_fn in company_labels]
    num_of_tweets_added = 0
    for com_lb in company_labels:
        print(com_lb, end=', ', flush=True)
        tweets = api.GetSearch(
            term=com_lb,
            since=search_start,
            until=search_end,
            count=100)
        time.sleep(9)
        for twt in tweets:
            twt = twt.AsDict()
            tweet_text = twt.get('full_text', '')
            favorite_count = twt.get('favorite_count', 0)
            created_at = twt.get('created_at', '')
            hashtag_list = twt.get('hashtags', [])
            hashtags = []
            for d in hashtag_list:
                h = d.get('text', '')
                if h:
                    hashtags.append(h)
            hashtags = ','.join(hashtags)
            tweet_id = twt.get('id_str', '')
            lang = twt.get('lang', '')
            url_list = twt.get('urls', [])
            urls = []
            for d in url_list:
                u = d.get('expanded_url', '')
                if u:
                    urls.append(u)
            urls = ','.join(urls)
            user = twt.get('user', {})
            user_followers = user.get('followers_count', 0)
            user_screen_name = user.get('screen_name', '')
            crawling_time = time.strftime('%Y-%m-%d|%H:%M')
            if re.search(pattern=r'\b' + com_lb.lower() +
                         r'\b', string=tweet_text.lower()):
                num_of_tweets_added += 1
                df.loc[df.shape[0], :] = \
                    (com_lb, tweet_text, favorite_count, created_at, hashtags,
                     tweet_id, lang, urls, user_followers, user_screen_name, crawling_time)
    print('Finished crawling...', time.strftime('%H:%M'))
    print('Added', num_of_tweets_added, 'to the dataset')
    if sym_or_fn == 'sym':
        df.to_csv('symbol_tweets.csv', index=False)
    else:
        df.to_csv('fullname_tweets.csv', index=False)


if sym_or_fn == 'sym':
    crawl_tweets(sym_or_fn, symbol_tweets_df)
else:
    crawl_tweets(sym_or_fn, fullname_tweets_df)

