import requests
from bs4 import BeautifulSoup
import urllib
import time
import os
import re

os.chdir(os.path.dirname(os.path.realpath(__file__)))

base_url = 'https://www.malaysiastock.biz/Market-Watch.aspx?type=A&value={}'
        
company_names = []
company_open_prices = []
company_high_prices = []
company_low_prices = []
company_last_prices = []
update_dates = []

# we will scrape the last price and the update data and time
# for each company
for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0":
    # create the url for the company after encoding the company
    # name to be valid for the url
    url = base_url.format(c)
    # download the web page of the company and get its HTML contents
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
               '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/72.0.3626.109 Safari/537.36'}
    html_doc = requests.get(url, headers=headers).text
    # parse the HTML contents using BeautifulSoup parser
    soup = BeautifulSoup(html_doc, 'html.parser')
    company_links = soup.select("tr > td.alignLeft > span > a")
    for co in company_links:
        co_url = "https://www.malaysiastock.biz/" + co.get('href')
        print('Scraping', co_url)
        co_name = co.text
        co_html_doc =  requests.get(co_url, headers=headers).text
        co_soup = BeautifulSoup(co_html_doc, 'html.parser')
        last_price = co_soup.select_one('#MainContent_lbQuoteLast').text
        open_price = co_soup.select_one('#MainContent_lbQuoteOpen').text
        price_range = co_soup.select_one('#MainContent_lbDayRange').text
        low_price, high_price = price_range.split('-')
        update_date = co_soup.find("div", string=re.compile("Market Date")).text
        company_names.append(co_name)
        company_open_prices.append(open_price)
        company_high_prices.append(high_price)
        company_low_prices.append(low_price)
        company_last_prices.append(last_price)
        update_dates.append(update_date)
    
print(len(company_high_prices), len(company_names))

# save the scraped prices to a file whose name contains the
# current datetime
file_name = 'malaysiastock_prices_' + time.strftime('%d-%b-%Y_%H-%M') + '.txt'
with open(file_name, 'w') as f:
    for c, opp, hip, lop, lap, u in zip(company_names, company_open_prices, 
    company_high_prices, company_low_prices, company_last_prices, update_dates):
        f.write(c + ' : ' + opp + ' : ' + hip + ' : ' + lop + ' : ' + lap + ' : ' + ' [' + u + ']' + '\n')