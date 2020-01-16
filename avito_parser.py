import requests
import time
from bs4 import BeautifulSoup as bs
from ad import Ad
#from phone_grabber import Grabber
#import re


class AvitoParser:
    def __init__(self, pause_time, city, quest, depth):
        self.headers = {'accept': '*/*',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
                        }
        self.site_adress = 'https://www.avito.ru'
        self.session = requests.Session()
        self.pause_time = pause_time
        self.ads_list = []
        self.parsed_pages = 0
        self.quest = quest
        self.city = city
        self.depth = depth
        self.base_url = self.get_base_url()
        self.total_pages = self.get_pages(self.base_url)
        self.urls_list = self.gen_urls()

    def get_request(self, url):
        time.sleep(self.pause_time)
        request = self.session.get(url, headers=self.headers)
        if request.status_code != 200:
            raise Exception("FailedLoadingUrl")
        if request.url == "{0}/blocked".format(self.site_adress):
            raise Exception("IPHasBeenTemporaryBanned")
        return request

    def get_pages(self, url):
        request = self.get_request(url)
        soup = bs(request.content, 'html.parser')
        pages = soup.find('div', attrs={'class': 'pagination-pages'}).find_all('a', attrs={'class': 'pagination-page'})[-1]['href']
        return pages.split('=')[1].split('&')[0]

    def get_base_url(self):
        return "{}/{}/?q={}".format(self.site_adress, self.city, self.quest)

    def gen_urls(self):
        urls_list = []
        try:
            self.total_pages = int(self.total_pages)
        except:
            raise Exception("FailedCastTotalPagesToInt")

        for i in range(1, self.depth + 1):
            url = self.base_url + "&p={}".format(i)
            urls_list.append(url)
        return urls_list

    def parse_page(self, soup):
        divs = soup.find_all('div', attrs={'class': 'snippet-horizontal'})
        print('Amount of ads: {}'.format(len(divs)))

        for div in divs:
            ad = Ad(div)
            # json_ad = ad.to_json()
            self.ads_list.append(ad)
            # print(json_ad)
            # ad.print_info()
        self.parsed_pages += 1

    def parse_urls(self):
        for i in range(len(self.urls_list)):
            request = self.get_request(self.urls_list[i])
            soup = bs(request.content, 'html.parser')
            self.parse_page(soup)
