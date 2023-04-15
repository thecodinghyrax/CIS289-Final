from django.contrib import admin

# Register your models here.
from .models import Catagory, Component, Version

class CatagoryAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    
admin.site.register(Catagory, CatagoryAdmin)

    
class VersionAdmin(admin.ModelAdmin):
    fields = ["brand", "part_number", "image_name"]
    list_display = ["brand", "part_number", "image_name"]
    
admin.site.register(Version, VersionAdmin)


class ComponentAdmin(admin.ModelAdmin):
    fields = [
        "catagory",
        "version",
        "date",
        "retailer",
        "link"
    ]
    list_display = [
        "catagory",
        "version",
        "date",
        "retailer",
        "link"
    ]

    
admin.site.register(Component, ComponentAdmin)