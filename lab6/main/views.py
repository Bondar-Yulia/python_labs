from django.shortcuts import render
from .models import Manufacturer, Brand

def index(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'index.html', {'manufacturers': manufacturers})

def brands(request, manufacturer_id):
    brands = Brand.objects.filter(manufacturer_id=manufacturer_id)
    return render(request, 'brands.html', {'brands': brands})
