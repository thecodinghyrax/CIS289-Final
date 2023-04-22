from .models import Catagory, Merchant, Part, Price
from .newegg_scrape import NewEggData
from .memoryc_scrape import MemoryCData

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

    def create_part(self, cls):
        if cls.valid:
            try:
                part = Part.objects.create_part(cls)
                part.save()
                print("Saved successfully")
                return True
            except Exception as e:
                print(f"{part.long_name} not saved. {e}")
                return False
        return False


    def get_prices(self):
        return Price.objects.order_by("date")

    def get_prices_by_part_id(self, part_id):
        return Price.objects.filter(part=part_id)

    def get_price_by_id(self, id):
        return Price.objects.get(id=id)

    def create_newegg_scrape(self, request):
        url = request.POST['link']
        catagory = self.get_catagory_by_name(request.POST['catagory'])
        merchant = self.get_merchant_by_name('NewEgg')
        return NewEggData(url, catagory, merchant)
    
    def create_memoryc_scrape(self, request):
        raise NotImplementedError