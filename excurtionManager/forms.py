from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.template.loader import render_to_string
from models import Product, ProductQuotation, Excurtion

class ProductQuotationForm(forms.ModelForm):
    class Meta:
        model = ProductQuotation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
class ExcurtionForm(forms.ModelForm):
    class Meta:
        model = Excurtion

        