from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),

    path('customer/<str:name>/', views.customer, name= 'customer'),
    path('product/<str:id>', views.product, name = 'product'),
    path('wishlist/<str:id>', views.add_to_favorite, name='favor'),
    path('addtocart/<str:id>', views.add_to_cart, name='add_to_cart'),
    path('cart/<str:name>', views.cart, name='cart'),
    path('buy/<str:id>', views.buy, name='buy'),
    path('rent/<str:id>', views.rent, name='rent'),

    path('category/<str:name>', views.category, name='category'),
    
    path('search', views.search, name='search'),
    path('delete/<str:name>/<str:type>', views.delete_cart_item, name='delete'),
    path('purchase', views.purchase, name='purchase'),
] 