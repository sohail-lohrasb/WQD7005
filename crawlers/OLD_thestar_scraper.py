import requests
from bs4 import BeautifulSoup
import urllib
import time
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

base_url = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter={}'

# reading the company names into a list
company_names = []
with open("company_names.txt") as f:
    for line in f:
        company_names.append(line.strip())
        
company_open_prices = []
company_high_prices = []
company_low_prices = []
company_last_prices = []
update_datetimes = []

# we will scrape the last price and the update data and time
# for each company
for c in company_names:
    # create the url for the company after encoding the company
    # name to be valid for the url
    url = base_url.format(urllib.parse.quote(c))
    print('Scraping: ' + url)
    # download the web page of the company and get its HTML contents
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
               '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/72.0.3626.109 Safari/537.36'}
    html_doc = requests.get(url, headers=headers).text
    # parse the HTML contents using BeautifulSoup parser
    soup = BeautifulSoup(html_doc, 'html.parser')
    # get the open price of the company
    open_price = soup.select_one('#slcontent_0_ileft_0_opentext').text
    # get the high price of the company
    high_price = soup.select_one('#slcontent_0_ileft_0_hightext').text
    # get the low price of the company
    low_price = soup.select_one('#slcontent_0_ileft_0_lowtext').text
    # get the last price of the company
    last_price = soup.select_one('#slcontent_0_ileft_0_lastdonetext').text
    # get the update date of the data
    update_date = soup.select_one('#slcontent_0_ileft_0_datetxt').text
    # get the update time of the data
    update_time = soup.select_one('#slcontent_0_ileft_0_timetxt').text
    # add the values to the corresponding lists
    company_open_prices.append(open_price)
    company_high_prices.append(high_price)
    company_low_prices.append(low_price)
    company_last_prices.append(last_price)
    update_datetimes.append(update_date + ' ' + update_time)

# save the scraped prices to a file whose name contains the
# current datetime
file_name = 'prices_' + time.strftime('%d-%b-%Y_%H-%M') + '.txt'
with open(file_name, 'w') as f:
    for c, opp, hip, lop, lap, u in zip(company_names, company_open_prices, 
    company_high_prices, company_low_prices, company_last_prices, update_datetimes):
        f.write(c + ' : ' + opp + ' : ' + hip + ' : ' + lop + ' : ' + lap + ' : ' + ' [' + u + ']' + '\n')