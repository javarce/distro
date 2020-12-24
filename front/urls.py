
from django.urls import path
from . import views


app_name = 'front'


urlpatterns = [
    path('', views.index, name='index'),
    path('/businesses', views.businesses, name='businesses'),
    path('/products', views.products, name='products'),
]
