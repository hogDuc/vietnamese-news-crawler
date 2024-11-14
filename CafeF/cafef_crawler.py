import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from tqdm import tqdm

cff = pd.DataFrame(
    {
        "muc": ["chung_khoan", "bds", 'doanh_nghiep', 'ngan_hang', 'vi_mo', "tcqt", 'thi_truong'],
        'id': [18831, 18832, 18833, 18834, 18835, 18836, 18839],
        'max_page': [10, 16, 13, 9, 10, 16, 15]
    }
)
cff = cff.set_index("muc")

def get_article(url):
    url_test = url
    html_test = BeautifulSoup(requests.get(url_test).content, 'html.parser')

    dateandcat = html_test.find("p", {"class":"dateandcat"})
    title = html_test.find("h1", {"data-role":"title"}).get_text().strip()
    date = datetime.strptime(
        dateandcat.find("span", {"class":"pdate"}).get_text()[:-4],
        '%d-%m-%Y - %H:%M'
    ).timestamp()
    description = html_test.find("h2", {"class": "sapo"}).get_text().strip()
    categ = dateandcat.find("a", {"data-role":"cate-name"}).get_text()

    body = [text.get_text().strip() for text in html_test.find("div", {"id":"mainContent"}).find_all("p")]
    body = ' '.join(body).replace("\n", "")
    return {"date": date, "title":title, "des": description, "categ": categ, "body": body}

def crawl_cafef(categ_id, max_page):
    article_urls = []
    for page in range(1, max_page + 1):
        url = f'https://cafef.vn/timelinelist/{categ_id}/{page}.chn'
        req = requests.get(url).content
        html = BeautifulSoup(req, "html.parser")
        article_urls.extend(['https://cafef.vn' + h3.find("a").get("href") for h3 in html.find_all("h3")])
    urls = []
    dates = []
    titles = []
    descs = []
    categs = []
    bodies = []
    # i = 0
    for url in tqdm(article_urls):
        # print(len(article_urls) - i , "articles remaining")
        try:
            data = get_article(url)
            if data["date"] < datetime.strptime('30/10/2024 00:00', '%d/%m/%Y %H:%M').timestamp():
                next
            else:
                urls.append(url)
                dates.append(data["date"])
                titles.append(data["title"])
                descs.append(data["des"])
                categs.append(data["categ"])
                bodies.append(data["body"])
                # i += 1
        except Exception as error:
            print(f'error at: ', url, error)

    dict = {
        'date': dates,
        # 'source' : 'cafef',
        'url' : urls,
        'title' : titles,
        'description' : descs,
        'category' : categs,
        'body' : bodies
    }
    data = pd.DataFrame(dict)
    data["source"] = "CafeF"
    return data

chung_khoan = crawl_cafef(
    cff.loc["chung_khoan", "id"],
    cff.loc["chung_khoan", "max_page"]
)
chung_khoan.to_csv("cafef_chung_khoan.csv", index= False)

bds = crawl_cafef(
    cff.loc["bds", "id"],
    cff.loc["bds", "max_page"]
)
bds.to_csv("cafef_bds.csv", index= False)

doanh_nghiep = crawl_cafef(
    cff.loc["doanh_nghiep", "id"],
    cff.loc["doanh_nghiep", "max_page"]
)
doanh_nghiep.to_csv('cafef_dn.csv', index= False)

ngan_hang = crawl_cafef(
    cff.loc["ngan_hang", "id"],
    cff.loc["ngan_hang", "max_page"]
)
ngan_hang.to_csv("cafef_ngan_hang.csv", index= False)

vi_mo = crawl_cafef(
    cff.loc["vi_mo", "id"],
    cff.loc["vi_mo", "max_page"]
)
vi_mo.to_csv("cafef_vi_mo.csv", index= False)

tcqt = crawl_cafef(
    cff.loc["tcqt", "id"],
    cff.loc["tcqt", "max_page"]
)
tcqt.to_csv("cafef_tcqt.csv", index= False)

thi_truong = crawl_cafef(
    cff.loc["thi_truong", "id"],
    cff.loc["thi_truong", "max_page"]
)
thi_truong.to_csv("cafef_thi_truong.csv", index= False)

cafef_news_data = pd.concat([chung_khoan, bds, doanh_nghiep, ngan_hang, vi_mo, tcqt, thi_truong])
cafef_news_data.to_csv("CafeF_data.csv")