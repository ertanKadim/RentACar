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
    path('account-dashboard/', views.account_dashboard, name='account_dashboard'),
    path('account-profile/', views.account_profile, name='account_profile'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('payment/', views.payment, name='payment'),
]