import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# lists to use to store scraped data
username = []
category = []
subscribers = []
total_videos = []
total_views = []
possible_link = []
description = []

# looping in the pages of channelcrawler.com
for i in range(51):  # bcs the number of webpage is until 50
    url = 'https://channelcrawler.com/eng/results/35096//page:{}/sort:Channel.subscribers/direction:desc'.format(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    youtubers = soup.findAll('div', {'class': 'channel col-xs-12 col-sm-4 col-lg-3'})

    for youtuber in youtubers:

        # scrape username
        user = youtuber.find('h4').get_text().strip()
        username.append(user)

        # scrape youtuber category
        categ = youtuber.find_all('b')[0].get_text().strip()
        category.append(categ)

        # scrape youtuber subcribers
        subsc = youtuber.find_all('p')[0].get_text().strip().split()[0]
        subscribers.append(subsc)

        # scrape youtuber total_videos
        tot_vid = youtuber.find_all('p')[0].get_text().strip().split()[2]
        total_videos.append(tot_vid)

        # scrape youtuber total_views
        tot_view = youtuber.find_all('p')[0].get_text().strip().split()[4]
        total_views.append(tot_view)

        # scrape youtuber link to his channel
        lnk = []
        poss_link = youtuber.find_all('h4')
        for link in poss_link:
            lnk.append(link.a['href'])
        possible_link.append(lnk)

        # scrape youtuber description
        dscr = []
        for descr in youtuber.find_all('a'):
            title1 = descr.get('title')
            dscr.append(title1)
        description.append(dscr)

# Create a dictionary
dict = {
    'username': username,
    'category': category,
    'subscribers': subscribers,
    'total_videos': total_videos,
    'total_views': total_views,
    'possible_link': possible_link,
    'description': description,
}

# Assign to dataframe
df = pd.DataFrame.from_dict(dict, orient='index')
df = df.transpose()

# some preprocessing
df['description'] = df['description'].astype('str')
df['description'] = df['description'].replace(r'\\n', ' ', regex=True)
df['description'] = df['description'].replace(to_replace=r'\\', value='', regex=True)

print(df)

# df.to_csv('Scraping youtubers.csv', index=False, encoding='utf-8-sig')
