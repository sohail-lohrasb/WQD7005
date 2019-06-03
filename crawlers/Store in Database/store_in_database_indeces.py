import pymysql
import pymysql.cursors
import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Asdlkj987!23',
                             db='data_mining_assignment',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

for file_name in os.listdir('data/indices'):
    with open('data/indices/' + file_name, encoding='utf-8-sig') as f:
        file_contents = [line.strip() for line in f.readlines()]
    for i in range(len(file_contents)):
        line_split = file_contents[i].split(',')
        index = line_split[0]
        last_price = line_split[1]
        high_price = line_split[2]
        low_price = line_split[3]
        update_datetime = line_split[4].strip('[]')
        update_date, update_time = update_datetime.split('|')
        update_date = update_date.replace('-', ' ')
        update_datetime = update_date + ' - ' + update_time
        try:
            with connection.cursor() as cursor:
                # Create new records
                sql = "INSERT INTO `Indices` (`Datetime`, `IndexName`, `LastPrice`, `HighPrice`,"\
                      " `LowPrice`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (update_datetime, index, last_price, high_price, low_price))
            connection.commit()
        except BaseException:
            print('Error while inserting a new entry into the database')
            print('File:', file_name, '| Line:', i+1)
    print('Finished inserting the contents of file:', file_name)
connection.close()
