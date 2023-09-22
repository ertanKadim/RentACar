from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')

def cars(request):
    return render(request, 'pages/cars.html')

def car_detail(request, slug):
    return render(request, 'pages/car_detail.html')