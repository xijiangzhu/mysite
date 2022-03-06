from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.index),
    path('login/',views.my_login),
    path('register/',views.my_register),
    path('logout/',views.my_logout),
]