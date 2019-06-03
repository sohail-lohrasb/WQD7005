import requests
from bs4 import BeautifulSoup
import os
import csv

for i in range(1,25):
    url = "https://www.thestar.com.my/news/latest/?tag=Business&pgno=" + str(i) + "#Latest"
    # create a "news_links.txt" file if does not exist to store the news links
    f = open("news_links.txt", "a+")
    f.close()

    # read the links from the file and put them in a list
    with open("news_links.txt") as f:
        news_links = f.read()
        news_links = news_links.splitlines()
        #news_links[-3:]

    # store thestar news front page css ids.
    news_ids = [
        '#slcontent_0_ileft_0_lvLastNews_ctrl0_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl1_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl2_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl3_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl4_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl5_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl6_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl7_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl8_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl9_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl10_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl11_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl12_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl13_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl14_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl15_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl16_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl17_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl18_hpHeadline',
        '#slcontent_0_ileft_0_lvLastNews_ctrl19_hpHeadline'
    ]


    # create different list that should be store from the site     
    links = []
    headlines = []
    categories = []
    dates = []
    timestamps = []
    stories = []



    # set the url of the site 
    #url = 'https://www.thestar.com.my/news/latest/?tag=Business'
    # download the web page of the news and get its HTML contents
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
               '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/72.0.3626.109 Safari/537.36'}
    html_doc = requests.get(url, headers=headers).text
    # parse the HTML contents using BeautifulSoup parser
    soup = BeautifulSoup(html_doc, 'html.parser')

    # checks if the news exist in the list
    # get the link and headline of news and update the file if the news does not exist
    for news_id in reversed(news_ids):
        news = soup.select_one(news_id)
        if news['href'] in news_links:
            print(news.text, "exists in the file")
        else:
            with open('news_links.txt', 'a') as f:
                f.write(news["href"])
                f.write("\n")
            links.append(news["href"])
            headlines.append(news.text)

    # go to the news page and get story, category, date and time of the news
    for link in links:
        new_html_doc = requests.get(link, headers=headers).text
        soup = BeautifulSoup(new_html_doc, 'html.parser')
        categories.append(soup.select_one('#side-note-article > li > a').text)
        dates.append(soup.select_one('.date').text.strip())
        timestamps.append(soup.select_one('.timestamp').text.strip())
        stories.append(soup.select_one('#slcontent_0_sleft_0_storyDiv').text.strip())
    
    # create a csv file and gather all the data to store in file    
    if not os.path.exists('./news.csv'):
        with open('news.csv', 'a', newline='') as f:
            fieldnames = ['link', 'headline', 'category', 'date', 'timestamp', 'story']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for link, headline, category, date, timestamp, story in zip(links, headlines, categories,
                                                                        dates, timestamps, stories):
                writer.writerow({'link':link, 'headline':headline, 'category':category,
                                 'date':date, 'timestamp':timestamp, 'story':story})
    else:
        with open('news.csv', 'a', newline='') as f:
            fieldnames = ['link', 'headline', 'category', 'date', 'timestamp', 'story']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for link, headline, category, date, timestamp, story in zip(links, headlines, categories,
                                                                        dates, timestamps, stories):
                writer.writerow({'link':link, 'headline':headline, 'category':category,
                                 'date':date, 'timestamp':timestamp, 'story':story})

