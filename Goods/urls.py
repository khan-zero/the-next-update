from django.urls import path, include
from Goods import views

app_name = 'shop'  

urlpatterns = [
    path('', views.main, name='main'),
    path('authentication/', include('Goods.authentication.urls', namespace='auth')),  # Authentication URLs 'auth' namespace bilan
    path('back-office/', include('Goods.back-office.urls')),  
    path('user/', include('Goods.user.urls', namespace='cart')),  
]

