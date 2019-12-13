from phone_grabber import Grabber


class Ad:
    def __init__(self, ad_soup):
        self.site = "avito.ru"

        try:
            self.id = ad_soup['id']
        except:
            self.id = "error"
            raise Exception("Failed parse id")
        try:
            self.href = ad_soup.find('a', attrs={'class': 'snippet-link'})['href']
        except:
            self.href = "error"
            raise Exception("Failed parse href")
        try:
            self.tittle = ad_soup.find('a', attrs={'class': 'snippet-link'}).text.strip()
        except:
            self.tittle = "error"
            raise Exception("Failed parse tittle") #?is it actually possible?
        try:
            self.date_published = ad_soup.find('ad_soup', attrs={'class': 'js-item-date c-2'})
        except:
            self.date_published = "error"
            #raise Exception("Failed parse date")
        try:
            self.price = ad_soup.find('span', attrs={'class': 'price'}).text.strip()
        except:
            self.price = "error"
            raise Exception("Failed parse price")

        self.adress = ""
        self.seller_name = ""
        self.description = ""
        self.seller_phone = ""

    def get_detailed_info(self, detailed_ad_soup):
        try:
            self.adress = detailed_ad_soup.find('span', attrs={'class': 'item-address__string'}).text
        except:
            self.adress = "error"
            raise Exception("Failed parse adress")
        try:
            self.seller_name = detailed_ad_soup.find('div', attrs={'class': 'seller-info-name'}).a.text
        except:
            self.seller_name = "error"
            raise Exception("Failed parse seller name")
        try:
            self.description = detailed_ad_soup.find('div', attrs={'class': 'item-description-text'})
        except:
            self.description = "error"
            raise Exception("Failed parse description")

    def get_phone_number(self):
        try:
            grabber = Grabber("avito.ru" + self.href)
            self.seller_phone = grabber.phone_number
        except:
            self.seller_phone = "error"
            raise Exception("Failed parse seller_phone")

    def print_info(self):
        print('id: {}\ntittle: {}\nPrice: {}\nAdress: {}\nSeller: {}'.format(self.id, self.tittle, self.price, self.adress, self.seller_name))
        print('Date published: {}'.format(self.date_published))
        print("Href: avito.ru{}".format(self.href))
        print("Description: {}".format(self.description))