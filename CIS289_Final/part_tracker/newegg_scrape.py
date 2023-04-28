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
        for script in self.scripts:
            try:
                intro = str(script)[:200]
                if 'Offer' in intro:
                    print(f"Intro: {intro}")
                    return json.loads(script.contents[0])
            except Exception as e:
                self.valid = False
                return None
        self.valid = False


    def get_price(self):
        try:
            price = self.data['offers']['price']
            return int(float(price) * 100)
        except Exception as e:
            self.valid = False
            return -1
    
    
    def get_long_name(self):
        try:
            return self.data['name']
        except Exception as e:
            self.valid = False
            return "Not Found"
    
    def get_brand(self):
        try:
            return self.data['brand']
        except Exception as e:
            self.valid = False
            return "Not Found"
    
    def get_image(self):
        try:
            return self.data['image']
        except Exception as e:
            self.valid = False
            return "Not Found"    
    
    def get_stock(self):
        try:
            stock = self.data['offers']['availability']
            if stock == 'http://schema.org/InStock':
                return True
            return False
        except Exception as e:
            self.valid = False
            return False
        
        
    def link_valid(self):
        return self.valid
    
    
    def get_data_dict(self):
        data = {
                "link" : self.url,
                "long_name": self.long_name,
                "brand" : self.brand,
                "image" : self.image,
                "catagory" : self.catagory,
                "merchant" : self.merchant,
                "valid" : self.valid,
                }
        return data

if __name__ == "__main__":
    pass

    