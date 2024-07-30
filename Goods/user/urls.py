from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.myCart, name='cart'),
    path('addProduct/', views.addProductToCart, name='addProduct'),
    path('subtract-from-cart/', views.substractProductFromCart, name='subtract_from_cart'),

]
