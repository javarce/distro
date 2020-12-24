
from django.shortcuts import render
from business.models import Business, Product


def index(request):
    businesses = Business.objects.all()[:3]
    products = Product.objects.all()[:10]
    context = { 'businesses': businesses, 'products': products }
    return render(request, 'front/home.html', context)


def businesses(request):
    businesses = Business.objects.all()
    context = { 'businesses': businesses }
    return render(request, 'front/business/list.html', context)


def products(request):
    products = Product.objects.all()
    context = { 'products': products }
    return render(request, 'front/catalog/product/list.html', context)
