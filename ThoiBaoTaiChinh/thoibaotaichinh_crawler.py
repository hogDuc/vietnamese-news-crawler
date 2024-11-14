import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from tqdm import tqdm

def get_article(url):
    article = BeautifulSoup(requests.get(url).content, 'html.parser')
    title = article.find('h1', {'class':'post-title'}).get_text().strip()
    date = datetime.strptime(
        article.find('span', {'class':'article-publish-time'}).get_text().strip(),
        '%H:%M | %d/%m/%Y' 
    ).timestamp()
    categ = article.find('a', {'class':'article-catname'}).get_text().strip()
    desc = article.find('div', {'class':'post-desc'}).get_text().strip()
    body = article.find('div', {'class':'post-content'}).get_text().strip()
    return {
        'date':date, 'title':title, 'desc':desc, 'categ':categ, 'body':body, 'source':'ThoiBaoTaiChinh'
    }

categories = ['kinh-te', 'tai-chinh', 'thue-hai-quan', 'chung-khoan', 
              'ngan-hang', 'bao-hiem', 'kinh-doanh', 'bat-dong-san', 
              'phap-luat', 'gia-ca']
pageIndex = []
for i in range(0, 100, 15):
    pageIndex.append(i)

all_urls = []
for category in categories:
    for index in pageIndex:
        url = f'https://thoibaotaichinhvietnam.vn/{category}&s_cond=&BRSR={index}'
        html = BeautifulSoup(
            requests.get(url).content, 'html.parser'
        )
        for a in html.find_all('article', {'class':'article'}):
            all_urls.append(a.find('a').get('href'))

dates = []
sources = []
urls = []
titles = []
descs = []
categs = []
bodies = []

for link in tqdm(all_urls):
    try:
        data = get_article(link)
        if data["date"] < datetime.strptime('30/10/2024 00:00', '%d/%m/%Y %H:%M').timestamp():
            next
        dates.append(data["date"])
        sources.append(data["source"])
        urls.append(link)
        titles.append(data["title"])
        descs.append(data["desc"])
        categs.append(data["desc"])
        bodies.append(data['body'])
    except Exception as error:
        print(f"Error at:, {link} {error}")

tbtt_data = pd.DataFrame({
        'date': dates,
        'source' : sources,
        'url' : urls,
        'title' : titles,
        'description' : descs,
        'category' : categs,
        'body' : bodies
    })

tbtt_data.to_csv("thoibaotaichinh_data.csv")