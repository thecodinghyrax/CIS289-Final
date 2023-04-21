from django import forms
from .models import Part, Catagory, Merchant

class PartForm(forms.ModelForm):
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all())
    merchant = forms.ModelChoiceField(queryset=Merchant.objects.all())
    class Meta:
        model = Part
        fields = ['catagory', 'merchant', 'link']
        labels = {
            'catagory' : "Catagory",
            'merchant' : "Merchant",
            'link' : "Link"
        }