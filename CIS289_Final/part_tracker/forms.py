from django import forms
from .models import Part, Catagory, Merchant

class PartForm(forms.ModelForm):
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all())
    merchant = forms.ModelChoiceField(queryset=Merchant.objects.all())
    class Meta:
        model = Part
        fields = ['catagory', 'merchant', 'name_from_user', 'link']
        labels = {
            'catagory' : "Catagory",
            'merchant' : "Merchant",
            'name_from_user' : 'Name of Part',
            'link' : "Link"
        }