from .models import Catagory, Merchant, Part, Price
import pandas as pd
from .newegg_scrape import NewEggData
from datetime import datetime

class Repository:

    def get_catagories(self):
        return Catagory.objects.order_by("-id")

    def get_catagory_by_name(self, name):
        return Catagory.objects.get(name=name)

    def get_catagory_by_id(self, id):
        return Catagory.objects.get(id=id)


    def get_merchants(self):
        return Merchant.objects.all()

    def get_merchant_by_name(self, name):
        return Merchant.objects.get(name=name)

    def get_merchant_by_id(self, id):
        return Merchant.objects.get(id=id)


    def get_parts(self):
        return Part.objects.all()

    def get_parts_by_catagory_name(self, catagory_name):
        catagory = self.get_catagory_by_name(catagory_name)
        return Part.objects.filter(catagory=catagory.id)

    def get_part_by_long_name(self, long_name):
        return Part.objects.filter(long_name=long_name)

    def get_part_by_id(self, id):
        return Part.objects.get(id=id)

    def create_part_from_scrape(self, part_dict):
        if part_dict["valid"]:
            try:
                part = Part.objects.create_part(part_dict)
                return part
            except Exception as e:
                print(f"Scrape could not be converted to Part. {e}")
                return None
        return None

    def del_part_by_id(self, id):
        self.get_part_by_id(id).delete()

    def get_prices(self):
        return Price.objects.values("price", "date", "part__long_name", "part__catagory__name").order_by("date")

    def get_prices_by_part_id(self, part_id):
        return Price.objects.filter(part=part_id)
    
    def get_prices_by_catagory(self, catagory):
            prices = Price.objects.values("price", "part_id", "part__long_name", "date", "part__catagory__name").filter(part__catagory__name=catagory)
            return pd.DataFrame.from_records(prices)
        
    def get_price_by_id(self, id):
        return Price.objects.get(id=id)

    def del_price_by_id(self, id):
        self.get_price_by_id(id).delete()

    def get_current_prices(self):
        unique_part_count = len(Price.objects.values('part_id').distinct())
        current_prices = Price.objects.all().values('part', 'price', 'date', 'part__catagory__name').order_by('-date')[:unique_part_count]
        print(f"Number of parts: {unique_part_count}")
        for price in current_prices:
            print(price)
        print(f"Length of Queryset: {len(current_prices)}")
        
        return current_prices
    
    def get_lowest_catagory_prices(self, current_prices):
        # I have fought this for half a day now. I was trying to use the django orm to 
        # get the current highest price for each unique catagory but I cant make it work. Pandas to the rescue
        current_prices_queryset = current_prices
        current_df = pd.DataFrame.from_records(current_prices_queryset)
        revised_df = current_df.sort_values('price', ascending=False).drop_duplicates('part__catagory__name').sort_index()
        revised_df['percentage'] = revised_df['price'] / revised_df['price'].sum() * 100

        return revised_df.to_dict()
        # https://docs.djangoproject.com/en/4.2/topics/db/queries/#expressions-can-reference-transforms
        

    def create_price_from_scrape(self, part, date):
        url = part.link
        catagory = part.catagory
        merchant = part.merchant
        data = NewEggData(url, catagory, merchant)
        price = Price()
        price.part = part
        price.price = data.get_price()
        price.date = date
        return price


    def create_newegg_scrape(self, request):
        url = request.POST['link']
        catagory = self.get_catagory_by_name(request.POST['catagory'])
        merchant = self.get_merchant_by_name('NewEgg')
        return NewEggData(url, catagory, merchant)
    
    