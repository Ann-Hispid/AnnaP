import logging
import time

import requests
from bs4 import BeautifulSoup

# Настройка логгера
logger = logging.getLogger('news_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('news.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s-%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def extract_news(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching the URL:{e}")
        return None, None, None

    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    title_element = soup.find('a', class_='list-item__title color-font-hover-only')
    tag_element = soup.find('span', class_='list-tag__text')
    date_element = soup.find('div', class_='list-item__date')

    title = title_element.text if title_element else "No title"
    annotation = tag_element.text if tag_element else "No annotation"
    date = date_element.text if date_element else "No date"

    return title, annotation, date

if __name__ == "__main__":
    url = 'https://ria.ru/lenta/'
    run_time = 4 * 60 * 60
    news_list = []
    start_time = time.time()

    while time.time() - start_time < run_time:
        title, tag, date = extract_news(url)
        if title and ('Россия' in title or 'Путин' in title or 'США' in title or 'Байден' in title or 'Трамп' in title or 'Росийские' in title or 'Президент' in title or 'ВСУ' in title):
            if len(news_list) == 0 or news_list[-1] != title:
                news_list.append(title)
                log_info = (title, tag, date)
                logger.info(log_info)
        time.sleep(60)