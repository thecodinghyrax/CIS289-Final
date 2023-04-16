from django.contrib import admin

# Register your models here.
from .models import Catagory, MerchantPart, PartModel, Merchant, Price

class CatagoryAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    
admin.site.register(Catagory, CatagoryAdmin)

    
class PartModelAdmin(admin.ModelAdmin):
    fields = ["catagory", "name_from_user", "long_name", "brand", "image_name"]
    list_display = ["catagory", "name_from_user", "long_name", "brand", "image_name"]
    
admin.site.register(PartModel, PartModelAdmin)


class MerchantAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]

admin.site.register(Merchant, MerchantAdmin)


class MerchantPartAdmin(admin.ModelAdmin):
    fields = [
        "model",
        "merchant",
        "link"
    ]
    list_display = [
        "model",
        "merchant",
        "link"
    ]

    
admin.site.register(MerchantPart, MerchantPartAdmin)

class PriceAdmin(admin.ModelAdmin):
    fields = [
        "merchant_part",
        "price",
        "date"
    ]
    list_display = [
        "merchant_part",
        "price",
        "date"
    ]

admin.site.register(Price, PriceAdmin)

