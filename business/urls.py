
from django.urls import path
from . import views


app_name = 'business'


urlpatterns = [
    path('', views.index, name='index'),
    path('/login', views.login, name='login'),
    path('/register', views.register, name='register'),
    path('/dashboard', views.dashboard, name='dashboard'),
]