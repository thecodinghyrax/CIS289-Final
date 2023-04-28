from .models import Catagory, Merchant, Part, Price
import pandas as pd
from .newegg_scrape import NewEggData
from datetime import datetime

class Repository:

    def get_catagories(self):
        '''
        Gets a queryset of all catagories in the database sorted by ID
        :returns: The sorted catagories queryset
        '''
        return Catagory.objects.order_by("-id")

    def get_catagory_by_name(self, name):
        '''
        Gets a queryset of a specific catagory in the database by it's name
        :returns: The catagory queryset that matches name
        '''
        return Catagory.objects.get(name=name)

    def get_catagory_by_id(self, id):
        '''
        Gets a queryset of a specific catagory in the database by it's id
        :returns: The catagory queryset that matches id
        '''
        return Catagory.objects.get(id=id)


    def get_merchants(self):
        '''
        Gets a queryset of all merchants in the database. Currently this is 
        only for NewEgg but more could be added. 
        :returns: The queryset of all merchants
        '''
        return Merchant.objects.all()

    def get_merchant_by_name(self, name):
        '''
        Gets a queryset of a specific merchant in the database by it's name
        :returns: The merchant queryset that matches name
        '''
        return Merchant.objects.get(name=name)

    def get_merchant_by_id(self, id):
        '''
        Gets a queryset of a specific merchant in the database by it's id
        :returns: The merchant queryset that matches id
        '''
        return Merchant.objects.get(id=id)


    def get_parts(self):
        '''
        Gets a queryset of all parts in the database
        :returns: The queryset of all parts
        '''
        return Part.objects.all()

    def get_parts_by_catagory_name(self, catagory_name):
        '''
        Gets a queryset of all parts in the supplied catagory found in the database
        :returns: The parts queryset that are found in the supplied catagory name
        '''
        catagory = self.get_catagory_by_name(catagory_name)
        return Part.objects.filter(catagory=catagory.id)

    def get_part_by_long_name(self, long_name):
        '''
        Gets a queryset of all parts in found in the database that have a matching long name
        :returns: The parts queryset that have a matching long name
        '''
        return Part.objects.filter(long_name=long_name)

    def get_part_by_id(self, id):
        '''
        Gets a queryset of a specific part in the database by it's id
        :returns: The part queryset that matches id
        '''
        return Part.objects.get(id=id)

    def create_part_from_scrape(self, part_dict):
        '''
        Creates a Part object from the supplied dictonary (if valid) and returns it 
        :param part_dict: A dictonary of part information from scrapeing 
        :returns: A Part object if successful, else None
        '''
        if part_dict["valid"]:
            try:
                part = Part.objects.create_part(part_dict)
                return part
            except Exception as e:
                return None
        return None

    def del_part_by_id(self, id):
        '''
        Deletes a specific part in the database by it's id
        '''
        try:
            self.get_part_by_id(id).delete()
        except Exception as e:
            print(f"{id} could not be deleted")

    def get_prices(self):
        '''
        Gets a queryset of all prices in the database orderd by date 
        :returns: The queryset of all prices ordered by date
        '''
        return Price.objects.values("price", "date", "part__long_name", "part__catagory__name").order_by("date")

    def get_prices_by_part_id(self, part_id):
        '''
        Gets a queryset of all prices that match part_id
        :returns: The price queryset that matches part_id
        '''
        return Price.objects.filter(part=part_id)
        
    def get_price_by_id(self, id):
        '''
        Gets a queryset of a specific price in the database by it's id
        :returns: The price queryset that matches id
        '''
        return Price.objects.get(id=id)
    
    def get_prices_by_catagory(self, catagory):
        '''
        Creates a dataframe from all prices that match catagory
        :param catagory: An instance of the catagory class
        :returns: A dataframe of all catagory prices
        '''
        prices = Price.objects.values("price", "part_id", "part__long_name", "date", "part__catagory__name").filter(part__catagory__name=catagory)
        return pd.DataFrame.from_records(prices)

    def del_price_by_id(self, id):
        '''
        Deletes a specific price in the database by it's id
        '''
        try:
            self.get_price_by_id(id).delete()
        except Exception as e:
            print(f"{id} could not be deleted")

    def get_current_prices(self):
        '''
        Get a queryset of all the most recent prices for each part in the database 
        First a unique list of parts is created, then all prices are returned ordered by
        date and then only the number of parts is retured (thus eliminating all older part prices )
        :returns: A Price queryset with only the newest prices for each part.
        '''
        unique_part_count = len(Price.objects.values('part_id').distinct())
        current_prices = Price.objects.all().values('part', 'price', 'date', 'part__catagory__name').order_by('-date')[:unique_part_count]

        return current_prices
    
    def get_lowest_catagory_prices(self, current_prices):
        '''
        Takes in the current prices as a queryset and converts it to a dataframe.
        The dataframe is then sorted by price and then all duplicated catagories is dropped.
        This will leave the highest price part from each catagory. A precentage column is then added
        to the dataframe and a percentage of the total is calculated for each catagory. This will be
        used in a pie chart. 
        :param current_price: A Price queryset with only the newest prices for each part.
        :returns: A dictonary of the highest prices for each catagory and their percentages of the total
        '''
        # I have fought this for half a day now. I was trying to use the django orm to 
        # get the current highest price for each unique catagory but I cant make it work. Pandas to the rescue
        current_prices_queryset = current_prices
        current_df = pd.DataFrame.from_records(current_prices_queryset)
        revised_df = current_df.sort_values('price', ascending=False).drop_duplicates('part__catagory__name').sort_index()
        revised_df['percentage'] = revised_df['price'] / revised_df['price'].sum() * 100

        return revised_df.to_dict()
        

    def create_price_from_scrape(self, part, date):
        '''
        Creates a price object using a part object and date to scrape NewEgg
        :param part: A Part object to find a current price for
        :param date: Todays date
        :returns: A Price object with the current price of the supplied part
        '''
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
        '''
        Creates an instance of NewEggData from a request. The NewEggData instance
        is responsible to scrapeing the data from NewEgg using the supplied part link
        :param request: A request object that contains a link to the part 
        :returns: An instance of NewEggData with the part data 
        '''
        url = request.POST['link']
        catagory = self.get_catagory_by_name(request.POST['catagory'])
        merchant = self.get_merchant_by_name('NewEgg')
        return NewEggData(url, catagory, merchant)
    
    