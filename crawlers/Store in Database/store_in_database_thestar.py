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

for file_name in os.listdir('data/thestar prices'):
    with open('data/thestar prices/' + file_name) as f:
        file_contents = [line.strip() for line in f.readlines()]
    for i in range(len(file_contents)):
        # extracting data from text files
        # example: ['3A', '0.840', '0.855', '0.840', '0.855', ' ']
        line_split = file_contents[i].split('[')
        symbol_prices = line_split[0].split(' : ')
        # remove last item which is just a space char
        symbol_prices = symbol_prices[:-1]
        # getting the company symbol
        company_symbol = symbol_prices[0]
        # getting the prices
        prices = symbol_prices[1:]
        # convert each price from a string to a float number
        prices = [float(x) if x != '-' else None for x in prices]
        open_price = prices[0]
        high_price = prices[1]
        low_price = prices[2]
        last_price = prices[3]
        # example: Updated : 08 Mar 2019 | 7:11 PM
        update_datetime = line_split[1].strip(']')
        # getting the update date
        update_date_search = re.search(r'\: (\d+ \w+ \d+) \|', update_datetime)
        if update_date_search:
            update_date = update_date_search.group(1)
        # getting the update time
        update_time_search = re.search(
            r'\| (\d+\:\d+ \w{2})$', update_datetime)
        if update_time_search:
            update_time = update_time_search.group(1)
        update_datetime = update_date + ' - ' + update_time
        try:
            with connection.cursor() as cursor:
                # Create new records
                sql = "INSERT INTO `TheStarData` (`Datetime`, `CompanySymbol`, `OpenPrice`, `HighPrice`,"\
                      " `LowPrice`, `LastPrice`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (update_datetime, company_symbol, open_price, high_price, low_price, last_price))
            connection.commit()
        except BaseException:
            print('Error while inserting a new entry into the database')
            print('File:', file_name, '| Line:', i+1)
connection.close()
