import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from tqdm import tqdm
# CONST

def get_article(url):
    html = BeautifulSoup(requests.get(url).content, 'html.parser')
    title = html.find('h1', {"class":'article__header'}).get_text().strip()
    date = html.find('time', {'class':'time'}).get('data-time')
    desc = html.find('div', {'class':'article__sapo'}).get_text().strip()
    categ = html.find('li', {'class':'main-cate'}).find('a').get('title')
    body = html.find('div', {'class':'article__body'}).get_text().strip().replace('\n',"")
    return {
        'date':date, 'title':title, 'desc':desc, 'categ':categ, 'body':body, 'source':'TinNhanhChungKhoan'
    }

categ_dict = {
    'chung-khoan':1,
    'thoi-su':7,
    'doanh-nghiep':4,
    'bat-dong-san':2,
    'quoc-te':9,
    'tai-chinh':60
}

min_date = datetime.strptime("30/11/2024", '%d/%m/%Y').timestamp()

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'origin': 'https://www.tinnhanhchungkhoan.vn',
    'priority': 'u=1, i',
    'referer': 'https://www.tinnhanhchungkhoan.vn/',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
}

params = {
    'phrase': '',
}

all_urls = []
page = 1
for categID in tqdm(list(categ_dict.keys())):
    while page > 0:
        response = requests.get(
            f'https://api.tinnhanhchungkhoan.vn/api/morenews-zone-{categ_dict[categID]}-{page}.html', 
            params=params, 
            headers=headers
        ).json()["data"]["contents"]
        urls = ['https://www.tinnhanhchungkhoan.vn' + element['url'] for element in response]
        all_urls.extend(urls)
        if response[-1]["date"] < min_date:
            print(f"Min date reached for {categID}")
            break
        else:
            page += 1

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
        dates.append(data["date"])
        sources.append(data["source"])
        urls.append(link)
        titles.append(data["title"])
        descs.append(data["desc"])
        categs.append(data["desc"])
        bodies.append(data['body'])
    except Exception as error:
        print(f"Error at:, {link} {error}")

tnck_data = pd.DataFrame({
        'date': dates,
        'source' : sources,
        'url' : urls,
        'title' : titles,
        'description' : descs,
        'category' : categs,
        'body' : bodies
    })
    
tnck_data.to_csv("tnck_data.csv")