from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('car/<slug:slug>/', views.car_detail, name='car_detail'),
]