from django.contrib import admin

# Register your models here.
from .models import Catagory, Part, Merchant, Price

class CatagoryAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    
admin.site.register(Catagory, CatagoryAdmin)

    
class PartAdmin(admin.ModelAdmin):
    fields = ["link", "long_name", "brand", "image", "catagory", "merchant"]
    list_display = ["link", "long_name", "brand", "image", "catagory", "merchant"]
    
admin.site.register(Part, PartAdmin)


class MerchantAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]

admin.site.register(Merchant, MerchantAdmin)


# class MerchantPartAdmin(admin.ModelAdmin):
#     fields = [
#         "model",
#         "merchant",
#         "link"
#     ]
#     list_display = [
#         "model",
#         "merchant",
#         "link"
#     ]

    
# admin.site.register(MerchantPart, MerchantPartAdmin)

class PriceAdmin(admin.ModelAdmin):
    fields = [
        "part",
        "price",
        "date"
    ]
    list_display = [
        "part",
        "price",
        "date"
    ]

admin.site.register(Price, PriceAdmin)

