from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Catagory
from .forms import PartModelForm


# Create your views here.
def index(request):
    catagories = Catagory.objects.order_by("-id")
    context = {"catagories": catagories}
    return render(request, "part_tracker/index.html", context)

def form(request):
    if request.method == "POST":
        form = PartModelForm(request.POST or None)
        if form.is_valid():
            print("Saving")
            form.save()
            form = PartModelForm()
        else:
            print("Invalid form")
            print(form.data)
    else:
        form = PartModelForm()
    return render(request, "part_tracker/form.html", {'form':form})
    