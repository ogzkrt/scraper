import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
import random


def get_data(url: str):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ua = UserAgent()
    hdr = {'User-Agent': ua.random,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    r = requests.get(url, headers=hdr, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find('tbody').find_all('tr')
    result = []
    for r in data:
        columns = r.find_all('td')
        if columns[0].text.strip() == 'TOPLAM':
            continue
        tmp = {
            'name': columns[0].text.strip().split('-->')[0].strip(),
            'capacity': int(columns[1].text.replace('.', '')),
            'filled_percentage': float(columns[2].text)
        }
        result.append(tmp)
    return result


def get_all_cities(urls):
    cities = []
    for u in urls:
        tmp = {
            'name': u['name'],
            'data': get_data(u['url'])
        }
        cities.append(tmp)
    return {
        'date': datetime.now(),
        'cities': cities
    }


def scrape():
    ankara_url = 'https://www.turkiye.gov.tr/asvk-baraj-doluluk-oranlari'
    istanbul_url = 'https://www.turkiye.gov.tr/istanbul-su-ve-kanalizasyon-idaresi-baraj-doluluk-oranlari'
    izmir_url = 'https://www.turkiye.gov.tr/izmir-su-ve-kanalizasyon-idaresi-baraj-doluluk-oranlari?hizmet=Ekrani'
    trabzon_url = 'https://www.turkiye.gov.tr/trabzon-icmesuyu-ve-kanalizasyon-idaresi-baraj-doluluk-oranlari-sorgulama?hizmet=Ekrani'

    urls = [
        {
            'name': 'ankara',
            'url': ankara_url
        },
        {
            'name': 'istanbul',
            'url': istanbul_url
        },
        {
            'name': 'izmir',
            'url': izmir_url
        },
        {
            'name': 'trabzon',
            'url': trabzon_url
        }
    ]

    print('Scraping data...')
    return get_all_cities(urls)


print(scrape())
