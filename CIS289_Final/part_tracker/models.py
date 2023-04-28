from django.db import models

# to load initial data into the database run this command:
# python manage.py loaddata initial_data


# Create your models here.
# This will be unchanged by the user
class Catagory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# This will be unchanged by the user
class Merchant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PartManager(models.Manager):
    def create_part(self, data_dict):
        part = self.create(link=data_dict['link'],
                           long_name=data_dict['long_name'],
                           brand=data_dict['brand'],
                           image=data_dict['image'],
                           catagory=data_dict['catagory'],
                           merchant=data_dict['merchant'],)
        return part

# The Part will be created based in information scraped from the Newegg link
# provided by the user
class Part(models.Model):
    link = models.CharField(max_length=2000)
    long_name = models.CharField(max_length=300, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=100, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    objects = PartManager()

    def __str__(self):
        return f"ID: {self.id} trunc name: {self.long_name[:20]}"


# Price will be entered by the scrapping code
class Price(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return '$' + '{:.2f}'.format(self.price * 0.01)
