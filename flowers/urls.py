from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_api, name='signup'),
    path('login/', login_api, name='login'),
    path('signout/', signout_api, name='signout'),
    path('cart/', cart, name='cart'),
    
]