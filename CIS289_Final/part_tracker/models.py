from django.db import models

# Create your models here.
# This will likely be unchanged by the user
class Catagory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
# The user will select the category and enter a name
# this data will be saved to the db and then the user will
# be prompted to select a merchant and a window will open in
# a seperate tab to the marchants website searching for the name
# The user will then copy the link they want and enter it as the
# merchantpart link. The scrap will then gather data for the rest of
# the partmodel and add a price.
class PartModel(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name_from_user = models.CharField(max_length=100)
    long_name = models.CharField(max_length=300, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    image_name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name_from_user
    
# This will likely be unchanged by the user
class Merchant(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# This will be added after the user gets the link they want
class MerchantPart(models.Model):
    model = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    link = models.CharField(max_length=2000)
    def __str__(self):
        return self.model.name_from_user + " - " + self.merchant.name
    

# Price will be entered by the scrapping code
class Price(models.Model):
    merchant_part = models.ForeignKey(MerchantPart, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    date = models.DateTimeField("Price Date")
    def __str__(self):
        return '$' + '{:.2f}'.format(self.price * 0.01)