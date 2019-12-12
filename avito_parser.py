import requests
import time
from bs4 import BeautifulSoup as bs
from ad import Ad
#from phone_grabber import Grabber
#import re


class FailedLoadingUrl(Exception):
    'if url not equals 200'
    pass


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:70.0) Gecko/20100101 Firefox/70.0'
           }

site = 'https://www.avito.ru'
base_url = 'https://www.avito.ru/volgograd/mebel_i_interer/krovati_divany_i_kresla?q=%D0%B4%D0%B8%D0%B2%D0%B0%D0%BD'
blocked_url = 'https://www.avito.ru/blocked'


def get_request(session, url, headers):
    request = session.get(url, headers=headers)
    if request.status_code != 200:
        raise Exception("FailedLoadingUrl")
    if request.url == blocked_url:
        raise Exception("IPHasBeenTemporaryBanned")
    return request


def get_pages(session, url, headers):
    request = get_request(session, url, headers)
    soup = bs(request.content, 'html.parser')
    pages = soup.find('div', attrs={'class': 'pagination-pages'}).find_all('a', attrs={'class': 'pagination-page'})[-1]['href']
    total_pages = pages.split('=')[1].split('&')[0]
    return total_pages


def gen_urls(url, pages):
    pass


def parse_avito(base_url, headers):
    session = requests.Session()
    request = get_request(session, base_url, headers)#session.get(base_url, headers=headers)
    soup = bs(request.content, 'html.parser')
    time.sleep(2.5)
    divs = soup.find_all('div', attrs={'class': 'snippet-horizontal'})
    print('Amount of ads: {}'.format(len(divs)))

    for div in divs:
        ad = Ad(div)
        ad.print_info()
        ad_request = get_request(session, site + ad.href, headers)#session.get(site + ad.href, headers=headers)
        ad_soup = bs(ad_request.content, 'html.parser')
        ad.get_detailed_info(ad_soup)
        time.sleep(11.5)
    #         item_request = session.get(href, headers=headers)
    #         if item_request.status_code == 200:
    #             print('ok2')
    #             item_soup = bs(item_request.content, 'html.parser')
    #             time.sleep(4)
    #             try:
    #                 tittle = item_soup.find('h1', attrs={'class': 'title-info-title'}).text.strip()
    #             except:
    #                 tittle = 'default'
    #
    #             try:
    #                 price = item_soup.find('span', attrs={'class': 'price-value-string'}).text.strip()
    #             except:
    #                 price = 'default'
    #
    #             try:
    #                 adress = item_soup.find('span', attrs={'class': 'item-address__string'}).text.strip()
    #             except:
    #                 adress = 'default'
    #
    #             try:
    #                 description = item_soup.find('div', attrs={'class': 'item-description-text'}).text.strip()
    #             except:
    #                 description = 'default'
    #
    #             try:
    #                 seller_name = item_soup.find('div', attrs={'class': 'seller-info-name'}).text.strip()
    #             except:
    #                 seller_name = 'default'
    #
    #             try:
    #                 map_coords = item_soup.find('div', attrs={'class': 'b-search-map'})
    #             except:
    #                 map_coords = None
    #
    #             try:
    #                 data_map_lat = map_coords['data-map-lat']
    #                 data_map_lon = map_coords['data-map-lon']
    #             except:
    #                 data_map_lat = 'default'
    #                 data_map_lon = 'default'
    #
    #             try:
    #                 date_published = item_soup.find('div',
    #                                                 attrs={'class': 'title-info-metadata-item-redesign'}).text.strip()
    #             except:
    #                 date_published = ''
    #
    #             print('tittle: {}\nPrice: {}\nAdress: {}\nSeller: {}'.format(tittle, price, adress, seller_name))
    #             print('Description: {}'.format(description))
    #             print('Coords: {} {}'.format(data_map_lat, data_map_lon))
    #             print('Date published: {}'.format(date_published))
    #
    #         else:
    #             print('error2')


parse_avito(base_url, headers)



#print('tittle: {}\nPrice: {}\nAdress: {}\nSeller: {}'.format(tittle, price, adress, seller_name))
#print('Description: {}'.format(description))
#print('Coords: {} {}'.format(data_map_lat, data_map_lon))
#print('Date published: {}'.format(date_published))
#print('Phone number: {}'.format(phone_number))