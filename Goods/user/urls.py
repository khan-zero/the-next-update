from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.myCart, name='cart'),
    path('addProduct/', views.addProductToCart, name='addProduct'),
    path('subtract-from-cart/', views.substractProductFromCart, name='subtract_from_cart'),

]
