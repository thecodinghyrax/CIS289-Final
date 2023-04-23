from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PartForm
from .repository import Repository


# Create your views here.
def index(request):
    repo = Repository()
    catagories = repo.get_catagories()
    parts = repo.get_parts()
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
    repo = Repository()
    if request.method == "POST":
        if "newegg" in request.POST['link'].lower():
            scraped_part = repo.create_newegg_scrape(request)
            if scraped_part.valid:
                try:
                    part = repo.create_part_from_scrape(scraped_part.get_data_dict())
                    part.save()
                    print("Saved to the database")
                except Exception as e:
                    print(e)
            else:
                print("Scrape is not valid")
        elif "memoryc" in request.POST['link'].lower():
            pass
    return HttpResponseRedirect('/')
    
def delPart(request):
    print(request.POST['id'])
    repo = Repository()
    if request.method == "POST":
        try:
            repo.del_part_by_id(request.POST['id'])
        except Exception as e:
            print(f"Could not delete {request.POST['id']}. {e}")
    return HttpResponseRedirect('/')