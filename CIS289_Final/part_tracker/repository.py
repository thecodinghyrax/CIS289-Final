from .models import Catagory, Merchant, Part, Price
from django.db.models import Max
from .newegg_scrape import NewEggData
from .memoryc_scrape import MemoryCData
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
                print(f"Scrap could not be converted to Part. {e}")
                return None
        return None

    def del_part_by_id(self, id):
        self.get_part_by_id(id).delete()

    def get_prices(self):
        return Price.objects.order_by("date")

    def get_prices_by_part_id(self, part_id):
        return Price.objects.filter(part=part_id)

    def get_price_by_id(self, id):
        return Price.objects.get(id=id)

    def del_price_by_id(self, id):
        self.get_price_by_id(id).delete()

    def get_current_prices(self):
        unique_part_count = Price.objects.values('part_id').distinct()
        current_prices = Price.objects.values('part_id', 'price').order_by('-date')[:len(unique_part_count)]
        return current_prices

    def create_price_from_scrape(self, part):
        url = part.link
        catagory = part.catagory
        merchant = part.merchant
        data = NewEggData(url, catagory, merchant)
        price = Price()
        price.part = part
        price.price = data.get_price()
        return price


    def create_newegg_scrape(self, request):
        url = request.POST['link']
        catagory = self.get_catagory_by_name(request.POST['catagory'])
        merchant = self.get_merchant_by_name('NewEgg')
        return NewEggData(url, catagory, merchant)
    

    def create_memoryc_scrape(self, request):
        raise NotImplementedError
    