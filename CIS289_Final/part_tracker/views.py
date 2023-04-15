from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    catagories = ["CPU", "GPU", "case", "PSU", "mother board", "storage", "OS", "RAM"]
    context = {"catagories": catagories}
    return render(request, "part_tracker/index.html", context)
