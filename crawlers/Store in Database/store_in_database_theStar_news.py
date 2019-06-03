import pymysql
import pymysql.cursors
import os
import re
import pandas as pd

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Asdlkj987!23',
                             db='data_mining_assignment',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

news_data = pd.read_csv('data/theStar_news.csv').reset_index(drop=True)

for i in range(news_data.shape[0]):
    news_item = news_data.iloc[i, :]
    link = news_item['link']
    headline = news_item['headline']
    category = news_item['category']
    date = news_item['date']
    time = news_item['timestamp']
    if pd.isna(time):
        time = None
    story = news_item['story']
    try:
        with connection.cursor() as cursor:
            # Create new records
            sql = "INSERT INTO `TheStarNews` (`Link`, `Headline`, `Category`, `Date`,"\
                " `Time`, `Story`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (link, headline, category, date, time, story))
        connection.commit()
    except BaseException:
        print('Error while inserting a new entry into the database')
        print(BaseException)
connection.close()
