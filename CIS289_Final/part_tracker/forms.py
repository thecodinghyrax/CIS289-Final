from django import forms
from .models import Part, Catagory

class PartForm(forms.ModelForm):
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all())
    class Meta:
        model = Part
        fields = ['catagory', 'name_from_user']
        labels = {
            'catagory' : "Catagory",
            'name_from_user' : 'Name of Part'
        }