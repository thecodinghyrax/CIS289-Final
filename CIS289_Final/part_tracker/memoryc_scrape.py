from bs4 import BeautifulSoup as bs
import json
import requests


class MemoryCData:
    def __init__(self, url):
        self.page = requests.get(url)
        self.soup = bs(self.page.content, 'html.parser')
        # self.scripts = self.soup.find_all(name='script')
        # self.data = self.get_data()
        
        
    def get_data(self):
        for script in self.scripts:
            intro = str(script)[:200]
            if 'Offer' in intro:
                return json.loads(script.contents[0])


    def get_price(self):
        try:
            elements = self.soup.find_all('quadpay-widget-v3')
            return elements[0]['amount']
        except Exception as e:
            print(f"price not found: {e}")
            return -1

    
    def get_long_name(self):
        try:
            element = self.soup.select('.forCartImageItem h1')
            for ele in element:
                text = ele.text.split('by')[0]
                return text
        except Exception as e:
            print(f"long name not found: {e}")
            return "Not Found"
    
    
    def get_short_name(self):
        try:
            split_name = self.get_long_name().split()
            short_name = " ".join(split_name[:4])
            return short_name
        except Exception as e:
            print(f"mpn not found: {e}")
            return "Not Found"
    
    
    def get_brand(self):
        try:
            element = self.soup.select('.forCartImageItem h1')
            for ele in element:
                text = ele.text.split('by')[1]
                return text
        except Exception as e:
            print(f"long name not found: {e}")
            return "Not Found"
    
    
    def get_image(self):
        try:
            return self.soup.select('link[rel="image_src"]')[0]['src']
        except Exception as e:
            print(f"image not found: {e}")
            return "Not Found"    
    
    
    def get_stock(self):
        return True
        
        
    def create_txt(self):
        with open('memoryC.txt', 'w', encoding='utf-8') as file:
            file.write(str(self.soup.prettify()))
            file.write("\n\n")


if __name__ == "__main__":
    mb_url = "https://www.memoryc.com/39224-msi-geforce-rtx-3060-ventus-2x-12g-oc-nvidia-12gb-gddr6-graphics-card.html?sscid=41k7_n2lff&"
    # mb_url = "https://www.memoryc.com/pc-components/cpus-processors/desktop/amd-ryzen-7-5800x-38ghz-l3-am4-cpu-desktop-processor-boxed.html"
    mb = MemoryCData(mb_url)
    # mb.create_txt()
    print(f"MB Price: {mb.get_price()}")
    print(f"MB Name: {mb.get_long_name()}")
    print(f"MB Short Name: {mb.get_short_name()}")
    print(f"MB Brand: {mb.get_brand()}")
    print(f"MB Image: {mb.get_image()}")
    print(f"MB Stock: {mb.get_stock()}")
    print()
    CPU_URL = "https://www.memoryc.com/pc-components/cpus-processors/desktop/amd-ryzen-7-5800x-38ghz-l3-am4-cpu-desktop-processor-boxed.html"
    CPU = MemoryCData(CPU_URL)
    print(f"CPU Price: {CPU.get_price()}")
    print(f"CPU Name: {CPU.get_long_name()}")
    print(f"CPU Short Name: {CPU.get_short_name()}")
    print(f"CPU Brand: {CPU.get_brand()}")
    print(f"CPU Image: {CPU.get_image()}")
    print(f"CPU Stock: {CPU.get_stock()}")

    