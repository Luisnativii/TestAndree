# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parking_info/', views.parking_info, name='parking_info'),
    path('car_enter/', views.car_enter, name='car_enter'),
    path('car_exit/', views.car_exit, name='car_exit'),
]