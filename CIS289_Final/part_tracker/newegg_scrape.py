from bs4 import BeautifulSoup as bs
import json
import requests


class NewEggData:
    def __init__(self, url):
        self.page = requests.get(url)
        self.soup = bs(self.page.content, 'html.parser')
        self.scripts = self.soup.find_all(name='script')
        self.data = self.get_data()
        
        
    def get_data(self):
        for script in self.scripts:
            intro = str(script)[:200]
            if 'Offer' in intro:
                return json.loads(script.contents[0])


    def get_price(self):
        try:
            price = self.data['offers']['price']
            return int(float(price) * 100)
        except Exception as e:
            print(f"price not found: {e}")
            return -1
    
    
    def get_long_name(self):
        try:
            return self.data['name']
        except Exception as e:
            print(f"short name not found: {e}")
            return "Not Found"
    
    def get_short_name(self):
        try:
            return self.data['mpn']
        except Exception as e:
            print(f"mpn not found: {e}")
            return "Not Found"
    
    def get_brand(self):
        try:
            return self.data['brand']
        except Exception as e:
            print(f"brand not found: {e}")
            return "Not Found"
    
    def get_image(self):
        try:
            return self.data['image']
        except Exception as e:
            print(f"image not found: {e}")
            return "Not Found"    
    
    def get_stock(self):
        try:
            stock = self.data['offers']['availability']
            if stock == 'http://schema.org/InStock':
                return True
            return False
        except Exception as e:
            print(f"mpn not found: {e}")
            return False

if __name__ == "__main__":
    pass

    