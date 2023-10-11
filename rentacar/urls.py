from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('car/<slug:slug>/', views.car_detail, name='car_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]