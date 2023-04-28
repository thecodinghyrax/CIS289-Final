from django.shortcuts import render
from django.http import HttpResponseRedirect
from .repository import Repository
from .charts import BudgetGraph
import threading
import datetime
import pytz
from django.contrib import messages


# Create your views here.
def index(request):
    repo = Repository()
    catagories = repo.get_catagories()
    parts = repo.get_parts()
    prices = repo.get_current_prices()
    graph = BudgetGraph(prices)
    pie = graph.graph_pie()
    lines = graph.create_price_charts()

    context = {
                "catagories": catagories,
                "parts" :parts,
                "prices" : prices,
                "pie" : pie,
                "lines" : lines
                }
    return render(request, "part_tracker/index.html", context)

def addPart(request):
    repo = Repository()
    if request.method == "POST":
        if "newegg" in request.POST['link'].lower():
            scraped_part = repo.create_newegg_scrape(request)
            if scraped_part.valid:
                try:
                    part = repo.create_part_from_scrape(scraped_part.get_data_dict())
                    part.save()
                    messages.success(request, f"New part successfully added!")
                except Exception as e:
                    messages.error(request, f"There was an error when trying to add this part. Error: {e}")
            else:
                messages.warning(request, f"There was an issue when trying to scrape this part. ")

        else:
            messages.error(request, f"This is not a valid NewEgg link. Please only use links from NewEgg.")
            
    return HttpResponseRedirect('/')
    
def delPart(request):
    repo = Repository()
    if request.method == "POST":
        try:
            repo.del_part_by_id(request.POST['id'])
            messages.success(request, f"Part was successfully deleted!")
        except Exception as e:
            messages.error(request, f"Could not delete {request.POST['id']}. {e}")
    return HttpResponseRedirect('/')

def updatePrices(request):
    if request.method == "POST":
        repo = Repository()
        parts = repo.get_parts()
        date = datetime.datetime.now(pytz.timezone('UTC'))
    def update_part_price(part):
        try:
            price = repo.create_price_from_scrape(part, date)
            price.save()
            messages.success(request, f"Prices were succcessfully updated!")
        except Exception as e:
            messages.error(request, f"Could not update prices. Error: {e}")

    for part in parts:
        thread = threading.Thread(target=update_part_price, args=(part,))
        thread.start()

    return HttpResponseRedirect('/')
