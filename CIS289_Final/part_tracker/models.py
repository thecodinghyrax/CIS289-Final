from django.db import models

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Version(models.Model):
    brand = models.CharField(max_length=50)
    part_number = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.brand
    
class Component(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    date = models.DateTimeField("Price Date")
    retailer = models.CharField(max_length=50)
    link = models.CharField(max_length=2000)
    def __str__(self):
        return self.version.brand
    
    
    
    