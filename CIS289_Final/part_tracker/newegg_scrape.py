from bs4 import BeautifulSoup as bs
import json
import requests


class NewEggData:
    def __init__(self, url, catagory, merchant):
        self.url = url
        self.catagory = catagory
        self.merchant = merchant
        self.valid = True
        self.page = requests.get(url)
        self.soup = bs(self.page.content, 'html.parser')
        self.scripts = self.soup.find_all(name='script')
        self.data = self.get_data()
        self.price = self.get_price()
        self.long_name = self.get_long_name()
        self.brand = self.get_brand()
        self.image = self.get_image()

    def get_data(self):
        '''
        Parses the scraped scripts data for an 'offer' section. This will contain
        most of the data neeeded for this class. If it fails to find the 'offer'
        the valid flage is set to False indicating a bad scrape. 
        :returns: The part data from the scrape as json else None if invalid
        '''
        for script in self.scripts:
            try:
                intro = str(script)[:200]
                if 'Offer' in intro:
                    return json.loads(script.contents[0])
            except Exception as e:
                self.valid = False
                return None
        self.valid = False

    def get_price(self):
        '''
        This parses the scraped data for a price and returns it as an int 
        representation of the float price (19.99 -> 1999)
        :returns: The price as an int else -1 if invalid
        '''
        try:
            price = self.data['offers']['price']
            return int(float(price) * 100)
        except Exception as e:
            self.valid = False
            return -1

    def get_long_name(self):
        '''
        This parses the scraped data for the part name 
        :returns: The part name or "Not Found" if invalid
        '''
        try:
            return self.data['name']
        except Exception as e:
            self.valid = False
            return "Not Found"

    def get_brand(self):
        '''
        This parses the scraped data for the manufacturer name 
        :returns: The manufacturer name or "Not Found" if invalid
        '''
        try:
            return self.data['brand']
        except Exception as e:
            self.valid = False
            return "Not Found"

    def get_image(self):
        '''
        This parses the scraped data for the part image url 
        :returns: The part image url or "Not Found" if invalid
        '''
        try:
            return self.data['image']
        except Exception as e:
            self.valid = False
            return "Not Found"

    def get_stock(self):
        '''
        This parses the scraped data for the availabililty 
        :returns: True if the part is in stock else False
        '''
        try:
            stock = self.data['offers']['availability']
            if stock == 'http://schema.org/InStock':
                return True
            return False
        except Exception as e:
            self.valid = False
            return False

    def link_valid(self):
        '''
        Returns the value of self.valid. If any class initialization calls 
        faile, valid becomes False indicating a bad scrape
        :returns: True if the scrape was successful else False
        '''
        return self.valid

    def get_data_dict(self):
        '''
        Creates a dictonary of all the scraped part data
        :returns: The class data as a dict
        '''
        data = {
            "link": self.url,
            "long_name": self.long_name,
            "brand": self.brand,
            "image": self.image,
            "catagory": self.catagory,
            "merchant": self.merchant,
            "valid": self.valid,
        }
        return data


if __name__ == "__main__":
    pass
