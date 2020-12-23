
from django.shortcuts import render
from business.models import Business


def index(request):
    businesses = Business.objects.all()[:3]
    context = { 'businesses': businesses }
    return render(request, 'front/base.html', context)
