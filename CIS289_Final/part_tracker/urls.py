from django.urls import path

from . import views


app_name = "part_tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("addPart/", views.addPart, name="addPart"),
    path("form/", views.form, name="form"),
]