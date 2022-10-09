from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import warnings
import pandas as pd

warnings.filterwarnings('ignore')


def _extract_urls_from_html(html: str):
    doc_tree = BeautifulSoup(html, "html.parser")
    news_list = doc_tree.find_all("li", "archive-page__item _news")
    return list(f"https://lenta.ru{news.find('a')['href']}" for news in news_list)


def parse_article_html(html: str):
    doc_tree = BeautifulSoup(html, "html.parser")
    topic = doc_tree.find('span', class_='topic-body__title').text
    text = " ".join([t.text for t in doc_tree.find_all('p', class_='topic-body__content-text')])
    return [topic, text]


_from_date = datetime.strptime("30.09.2022", "%d.%m.%Y")


def get_request(url):
    i = 0
    while i < 5:
        try:
            return requests.get(url, verify=False, timeout=0.5).text
        except:
            i += 1
    return None


date_start, date_end = _from_date, datetime.today()
df = []
while date_start <= date_end:
    new_date = date_start.strftime("%Y/%m/%d")
    for i in range(4):
        if i == 0:
            news_page_url = "https://lenta.ru/news" + f"/{new_date}"
        else:
            news_page_url = "https://lenta.ru/news" + f"/{new_date}/page/{i + 1}/"

        print(news_page_url)

        html = get_request(news_page_url)
        if html is None:
            # date_start += timedelta(days=1)
            print('error')
            continue
        texts_new = _extract_urls_from_html(html)
        if len(texts_new) == 0:
            break
        for i in texts_new:
            new_html = get_request(i)
            if new_html is None:
                print('error')
                continue
            params = parse_article_html(new_html)
            df.append(params + [str(date_start.strftime("%Y/%m/%d"))])
    date_start += timedelta(days=1)
df = pd.DataFrame(df)
df.columns = ['title', 'text', 'date']
df.to_csv('test.csv', index=False)
