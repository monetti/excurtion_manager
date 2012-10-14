# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import Product

def detail_product(request, id):
    product = get_object_or_404(Product,pk=id)
    
    return render(
        request,
        'product_detail.html',
        {
            'product':product,
        }
    )