# Create your views here.
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, \
    render_to_response
from django.utils.html import escape
from excurtionManager.forms import ProductQuotationForm
from models import Product

def cotizar(request, id):
    product = get_object_or_404(Product,pk=id)
    
    if request.method == "POST":
        
        if request.POST['ganancia'] and request.POST['precio']:
            pass
        else:
            if request.POST['ganancia']:
                if float(request.POST['ganancia']) != 0.0:
                    product.percentage = float(request.POST['ganancia'])
                    product.price = product.precio_estimado() 
                    product.save()
            if request.POST['precio']:
                if float(request.POST['precio']) != 0.0:
                    product.price = float(request.POST['precio'])
                    product.percentage = 0.0
                    product.save()
    
    return redirect("/products/"+id)

def product_quotation_add_to_product(request):
    if request.method == "POST":
        form = ProductQuotationForm(request.POST)
        if form.is_valid():
            pq = form.save()
            obj = get_object_or_404(Product, pk=request.POST['id_product'])
            obj.product_quotation.add(pq)
            obj.save()
    return redirect("/products/"+request.POST['id_product'])

