import requests
import time
from bs4 import BeautifulSoup as bs
from ad import Ad
#from phone_grabber import Grabber
#import re


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
           }

site_adress = 'https://www.avito.ru'
#base_url = 'https://www.avito.ru/volgograd/mebel_i_interer/krovati_divany_i_kresla?q=%D0%B4%D0%B8%D0%B2%D0%B0%D0%BD'


def get_request(session, url, headers, pause_time=2.5):
    time.sleep(pause_time)
    request = session.get(url, headers=headers)
    if request.status_code != 200:
        raise Exception("FailedLoadingUrl")
    if request.url == "https://www.avito.ru/blocked":
        raise Exception("IPHasBeenTemporaryBanned")
    return request


def get_pages(session, url, headers):
    request = get_request(session, url, headers)
    soup = bs(request.content, 'html.parser')
    pages = soup.find('div', attrs={'class': 'pagination-pages'}).find_all('a', attrs={'class': 'pagination-page'})[-1]['href']
    total_pages = pages.split('=')[1].split('&')[0]
    return total_pages


def gen_urls(city, quest, pages):
    try:
        pages = int(pages)
    except:
        raise Exception("FailedCastPagesToInt")
    urls_list = []
    base_url = "https://www.avito.ru/{}/?q={}".format(city, quest)
    for i in range(1, pages + 1):
        url = base_url + "&p={}".format(i)
        urls_list.append(url)
    return urls_list


def parse_page(soup):
    divs = soup.find_all('div', attrs={'class': 'snippet-horizontal'})
    print('Amount of ads: {}'.format(len(divs)))

    for div in divs:
        ad = Ad(div)
        json_ad = ad.to_json()
        print(json_ad)
        #ad.print_info()


session = requests.Session()
quest = "диван"
city = "volgograd"
base_url = site_adress + "/{}/?q={}".format(city, quest)
pages = get_pages(session, base_url, headers)
urls_list = gen_urls(city, quest, pages)
for i in range(len(urls_list)):
    request = get_request(session, urls_list[i], headers)
    soup = bs(request.content, 'html.parser')
    parse_page(soup)


#print('tittle: {}\nPrice: {}\nAdress: {}\nSeller: {}'.format(tittle, price, adress, seller_name))
#print('Description: {}'.format(description))
#print('Coords: {} {}'.format(data_map_lat, data_map_lon))
#print('Date published: {}'.format(date_published))
#print('Phone number: {}'.format(phone_number))