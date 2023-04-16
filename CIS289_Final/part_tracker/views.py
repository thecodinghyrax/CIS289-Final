from django.shortcuts import render
from django.http import HttpResponse
from .models import Catagory


# Create your views here.
def index(request):
    catagories = Catagory.objects.order_by("-id")
    context = {"catagories": catagories}
    return render(request, "part_tracker/index.html", context)
