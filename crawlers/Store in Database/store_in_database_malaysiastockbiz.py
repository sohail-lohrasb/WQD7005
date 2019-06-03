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

for file_name in os.listdir('data/malaysiastockbiz prices'):
    with open('data/malaysiastockbiz prices/' + file_name) as f:
        file_contents = [line.strip() for line in f.readlines()]
    for i in range(len(file_contents)):
        # extracting data from text files
        line_split = file_contents[i].split('[')
        symbol_prices = line_split[0].split(' : ')
        # remove last item which is just a space char
        symbol_prices = symbol_prices[:-1]
        # getting the company symbol
        company_symbol = symbol_prices[0]
        # getting the prices
        prices = symbol_prices[1:]
        # convert each price from a string to a float number
        try:
            prices = [float(x) if re.search(r'^\s+\d+\.\d+\s+$', x) else None for x in prices]
        except BaseException:
            print('Error while conversion. File:', file_name)
            print(prices)
        open_price = prices[0]
        high_price = prices[1]
        low_price = prices[2]
        last_price = prices[3]
        update_date = line_split[1].strip(']')
        # getting the update date
        update_date_search = re.search(r'\: (\d+ \w+ \d+)$', update_date)
        if update_date_search:
            update_date = update_date_search.group(1)
        try:
            with connection.cursor() as cursor:
                # Create new records
                sql = "INSERT INTO `MalaysiastockbizData` (`Date`, `CompanySymbol`, `OpenPrice`, `HighPrice`,"\
                      " `LowPrice`, `LastPrice`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (update_date, company_symbol, open_price, high_price, low_price, last_price))
            connection.commit()
        except BaseException:
            print('Error while inserting a new entry into the database')
            print('File:', file_name, '| Line:', i+1)
    print('Finished inserting the contents of file:', file_name)
connection.close()
