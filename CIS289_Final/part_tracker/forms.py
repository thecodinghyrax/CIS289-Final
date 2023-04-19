from django import forms
from .models import PartModel, MerchantPart, Catagory

class PartModelForm(forms.ModelForm):
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all())
    class Meta:
        model = PartModel
        fields = ['catagory', 'name_from_user']
        labels = {
            'catagory' : "Catagory",
            'name_from_user' : 'Name of Part'
        }