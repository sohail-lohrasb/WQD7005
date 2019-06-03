import requests
from bs4 import BeautifulSoup
import urllib
import time
import os
import re

base_url = 'https://www.malaysiastock.biz/Market-Watch.aspx?type=A&value={}'
        

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0":
    url = base_url.format(letter)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
               '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/72.0.3626.109 Safari/537.36'}
    html_doc = requests.get(url, headers=headers).text
    
    main_soup = BeautifulSoup(html_doc, 'html.parser')
    company_links = main_soup.select("tr > td.alignLeft > span > a")
    for co in company_links:
        co_url = "https://www.malaysiastock.biz/" + co.get('href')
        print('Scraping', co_url)
        co_name = co.text
        co_html_doc =  requests.get(co_url, headers=headers).text
        soup = BeautifulSoup(co_html_doc, 'html.parser')
        
        #find table of financial reports
        test = soup.find_all('table', id="MainContent_gvReport")
        test_string = '>(.+?)</td'
        
        try:
            result = re.findall(test_string, str(test[0]))
            
            #extract variables
            try:
                for i in range(0,500,10):
                    date = result[i]
                    financial_year = re.findall('>(.+?)$',result[i+1])[0]
                    financial_quarter = re.findall('>(.+?)$',result[i+3])[0]
                    revenue = re.findall('>(.+?)$',result[i+4])[0].replace(',','')
                    pbt = re.findall('>(.+?)$',result[i+5])[0].replace(',','')
                    net_profit = re.findall('>(.+?)$',result[i+6])[0].replace(',','')
                    eps = re.findall('>(.+?)$',result[i+7])[0]
                    divident = re.findall('>(.+?)$',result[i+8])[0]
                    nta = re.findall('>(.+?)$',result[i+9])[0]

                    row = co_name + ',' + date + ',' + financial_year + ',' + financial_quarter + ',' + revenue + ',' + pbt + ',' + net_profit + ',' + eps + ',' + divident + ',' + nta
                    file = open("output.txt","a+")
                    file.write(row+'\n')
                    file.close()
            except:
                print('End of table reached!')
        except:
            print('Financial report not available for this company!')
        
        