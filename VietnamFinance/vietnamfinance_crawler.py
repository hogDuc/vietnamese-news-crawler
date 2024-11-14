import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from tqdm import tqdm

def get_article(url):
    html = BeautifulSoup(
        requests.get(url).content, 'html.parser'
    )
    title = html.find('h1', {'class':'detail-title mb-20'}).get_text().strip()
    date = html.find('div',{'class':'detail-time-public'}).find('span').get_text().strip()[:-8]
    desc = html.find('h2', {'class':'detail-sapo'}).get_text().strip()
    body = html.find('div', {'id':'news_detail'}).get_text().strip()
    categ = html.find('li', {'class':'breadcrumb-item'}).find('a').get_text().strip()
    return {
        'title':title, 'date':date, 'desc':desc, 'body':body, 'categ':categ, 'source':'VietnamFinance'
    }

cookies = {
    'cf_clearance': '6Ad8RJXKzxD82MjvxjlCUIq6562XW7_p9OyzNUSyvRE-1714989711-1.0.1.1-jZfVormzRhzQ2uvKthKL.K6Z.ychGdUfEPwvgKf6qUYRROe2WzDUcp3owldgM3lEjq.6vV6FW_OXs9MqticisQ',
    '_gid': 'GA1.2.300395600.1731375755',
    '_gat_gtag_UA_69723249_1': '1',
    '_ga': 'GA1.2.406924487.1730960927',
    '_ga_VB94C3HYT3': 'GS1.1.1731375752.6.1.1731375771.41.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'cf_clearance=6Ad8RJXKzxD82MjvxjlCUIq6562XW7_p9OyzNUSyvRE-1714989711-1.0.1.1-jZfVormzRhzQ2uvKthKL.K6Z.ychGdUfEPwvgKf6qUYRROe2WzDUcp3owldgM3lEjq.6vV6FW_OXs9MqticisQ; _gid=GA1.2.300395600.1731375755; _gat_gtag_UA_69723249_1=1; _ga=GA1.2.406924487.1730960927; _ga_VB94C3HYT3=GS1.1.1731375752.6.1.1731375771.41.0.0',
    'origin': 'https://vietnamfinance.vn',
    'priority': 'u=1, i',
    'referer': 'https://vietnamfinance.vn/tai-chinh/',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
}

categories = [3, 4, 11, 12, 22, 23, 17, 5]
current_time = datetime.strftime(datetime.now(), format= '%Y-%m-%d %H:%M:%S')
all_urls = []
for category in categories:
    for i in range(1, 100):
        params = {
            'mod': 'iframe',
            'act': 'loadCate',
            'page': f'{i}',
        }

        data = {
            # 'last_id': '118408',
            f'last_push': {current_time},
            'cate_id': {category},
        }

        response = requests.post('https://vietnamfinance.vn/', params=params, headers=headers, data=data)
        html = BeautifulSoup(response.text, 'html.parser')
        for link in html.find_all('a', {'class':'fix-text3'}):
            all_urls.append(link.get('href'))
        if datetime.strptime(
            html.find_all('div', {'cate_id':'3'})[-1].get('last_push'),
            '%Y-%m-%d %H:%M:%S'
        ).timestamp() < datetime.strptime('30/10/2024 00:00', '%d/%m/%Y %H:%M').timestamp():
            break
        else:
            continue

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
        if data['date'] < datetime.strptime('30/10/2024 00:00', '%d/%m/%Y %H:%M').timestamp():
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

vietnamfinance_data = pd.DataFrame({
        'date': dates,
        'source' : sources,
        'url' : urls,
        'title' : titles,
        'description' : descs,
        'category' : categs,
        'body' : bodies
    })
    
vietnamfinance_data.to_csv('vietnamfinance_data.csv')