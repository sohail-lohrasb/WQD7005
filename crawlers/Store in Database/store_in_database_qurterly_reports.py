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

with open('data/quarterlyreport.txt') as f:
    file_contents = [line.strip() for line in f.readlines()]
for i in range(len(file_contents)):
    # extracting data from text files
    line_split = file_contents[i].split(',')
    company_symbol = line_split[0]
    date = line_split[1]
    financial_year = line_split[2]
    financial_quarter = line_split[3]
    revenue = float(line_split[4])
    pbt = float(line_split[5])
    net_profit = float(line_split[6])
    eps = float(line_split[7])
    dividend = float(line_split[8])
    nta = float(line_split[9])
    try:
        with connection.cursor() as cursor:
            # Create new records
            sql = "INSERT INTO `QuarterlyReports` (`CompanySymbol`, `Date`, `FinancialYear`, `FinancialQuarter`,"\
                    " `Revenue_RM_000`, `PBT_RM_000`, `NetProfit_RM_000`, `EPS_Cent`, `Dividend_Cent`, `NTA_RM`)"\
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,
                            (company_symbol, date, financial_year, financial_quarter, revenue, pbt, net_profit, 
                            eps, dividend, nta))
        connection.commit()
    except BaseException:
        print('Error while inserting a new entry into the database')
connection.close()
