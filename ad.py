class Ad:
    def __init__(self, div):
        try:
            self.id = div['data-item-id']
        except:
            self.id = "err"
            print("Failed init id")
        try:
            self.href = div.find('a', attrs={'class': 'snippet-link'})['href']
        except:
            self.href = "err"
            raise Exception("Failed parse href")
        try:
            self.tittle = div.find('a', attrs={'class': 'snippet-link'}).text.strip()
        except:
            self.tittle = "err"
            raise Exception("Failed parse tittle") #?is it actually possible?
        try:
            self.date_published = div.find('div', attrs={'class': 'js-item-date c-2'})
        except:
            self.date_published = "err"
            raise Exception("Failed parse date")
        try:
            self.price = div.find('span', attrs={'class': 'price'}).text.strip()
        except:
            self.price = "err"
            raise Exception("Failed parse price")


        self.adress = ""
        self.seller_name = ""

    def print_info(self):
        print('tittle: {}\nPrice: {}\nAdress: {}\nSeller: {}'.format(self.tittle, self.price, self.adress, self.seller_name))
        print('Date published: {}'.format(self.date_published))
        print("Href: avito.ru{}".format(self.href))