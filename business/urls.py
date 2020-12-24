
from django.urls import path
from . import views


app_name = 'business'


urlpatterns = [
    path('', views.index, name='index'),
    path('/login', views.login, name='login'),
    path('/logout', views.logout, name='logout'),
    path('/register', views.register, name='register'),
    path('/dashboard', views.dashboard, name='dashboard'),
    path('/all', views.my_businesses, name='my_businesses'),
    path('/add', views.add_businesses, name='add_businesses'),
    path('/<int:business_id>/edit', views.edit_businesses, name='edit_businesses'),
    path('/current/<int:id>/activate', views.activate_business_session, name='activate_business_session'),
    path('/catalog/categories', views.categories, name='categories'),
    path('/catalog/category/add', views.add_category, name='add_category'),
    path('/catalog/category/<int:id>/edit', views.edit_category, name='edit_category'),
    path('/catalog/category/<int:id>/delete', views.delete_category, name='delete_category'),
    path('/catalog/products', views.products, name='products'),
    path('/catalog/product/add', views.add_product, name='add_product'),
    path('/catalog/product/<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('/catalog/product/<int:product_id>/delete', views.delete_product, name='delete_product'),
    path('/users/<int:role_id>/role', views.users, name='users'),
    path('/users/role/<int:role_id>/add', views.add_user, name='add_user'),
    path('/users/<int:user_id>/role/<int:role_id>/edit', views.edit_user, name='edit_user'),
    path('/users/<int:user_id>/role/<int:role_id>/delete', views.delete_user, name='delete_user'),
]
