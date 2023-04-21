from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Catagory, Merchant, Part
from .forms import PartForm
from .newegg_scrape import NewEggData
from .memoryc_scrape import MemoryCData
from .repository import Repository as repo


# Create your views here.
def index(request):
    
    catagories = Catagory.objects.order_by("-id")
    parts = Part.objects.all()
    context = {
                "catagories": catagories,
                "parts" :parts
                }
    return render(request, "part_tracker/index.html", context)

def form(request):
    if request.method == "POST":
        form = PartForm(request.POST or None)
        if form.is_valid():
            print("Saving")
            form.save()
            form = PartForm()
        else:
            print("Invalid form")
            print(form.data)
    else:
        form = PartForm()
    return render(request, "part_tracker/form.html", {'form':form})

def addPart(request):
    if request.method == "POST":
        url = request.POST['link']
        catagory = Catagory.objects.get(name=(request.POST['catagory']))
        merchant = Merchant.objects.get(name='NewEgg')
        if "newegg" in url.lower():
            scraped_part = NewEggData(url, catagory, merchant)
            if scraped_part.valid:
                try:
                    part = Part.objects.create_part(scraped_part.get_data_dict())
                    part.save()
                    print("Saved to the database")
                except Exception as e:
                    print(e)
            else:
                print("fail")
        elif "memoryc" in url.lower():
            pass
    return HttpResponseRedirect('/')
    