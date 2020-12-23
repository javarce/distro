
from django.urls import path
from . import views


app_name = 'business'


urlpatterns = [
    path('', views.index, name='index'),
    path('/login', views.login, name='login'),
    path('/register', views.register, name='register'),
    path('/dashboard', views.dashboard, name='dashboard'),
    path('/all', views.my_businesses, name='my_businesses'),
    path('/add', views.add_businesses, name='add_businesses'),
    path('/current/<int:id>/activate', views.activate_business_session, name='activate_business_session'),
    path('/catalog/categories', views.categories, name='categories'),
    path('/catalog/category/add', views.add_category, name='add_category'),
    path('/catalog/products', views.products, name='products'),
    path('/catalog/product/add', views.add_product, name='add_product'),
]
