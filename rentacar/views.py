from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking
from django.utils import timezone
from django.contrib import messages
import datetime
import json

def index(request):
    title = 'Anasayfa'

    cars = list(Car.objects.order_by('-created_at')[:5])

    return render(request, 'pages/index.html', {
        'title': title,
        'cars': cars,
    })

def cars(request):
    title = 'Kiralık Araçlar'
    cars = Car.objects.filter()
    return render(request, 'pages/cars.html', {
        'title': title,
        'cars': cars,
        'now': timezone.now(),
    })

def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    title = f"{car.brand} {car.model}"

    # Kiralanmış tarihleri al
    booked_dates = Booking.objects.filter(car=car).values_list('start_date', 'return_date', flat=False)

    booked_dates_list = []
    for start, end in booked_dates:
        current = start
        while current <= end:
            booked_dates_list.append(current.strftime('%Y-%m-%d'))
            current += datetime.timedelta(days=1)

    if request.method == 'POST':
        # Kullanıcının formdan gönderdiği tarihleri al
        start_date = request.POST.get('Pick Up Date')
        start_time = request.POST.get('Pick Up Time')
        return_date = request.POST.get('Collection Date')
        return_time = request.POST.get('Collection Time')
        pickup_location = request.POST.get('pickup_location')
        dropoff_location = request.POST.get('dropoff_location')

        # Tarihleri Python'un anlayabileceği formata dönüştür
        start_datetime = datetime.datetime.strptime(f"{start_date} {start_time}", "%d %B %Y %H:%M")
        return_datetime = datetime.datetime.strptime(f"{return_date} {return_time}", "%d %B %Y %H:%M")

        # Arabanın bu tarihlerde müsait olup olmadığını kontrol et
        if Booking.is_car_available(car, start_datetime.date(), return_datetime.date()):
            booking = Booking(
                car=car,
                start_date=start_datetime.date(),
                start_time=start_datetime.time(),
                return_date=return_datetime.date(),
                return_time=return_datetime.time(),
                pickup_location=pickup_location,
                dropoff_location=dropoff_location
            )
            booking.save()
            messages.success(request, 'Araba başarıyla kiralandı!')
            return redirect('car_detail', slug=slug)
        else:
            messages.error(request, 'Bu tarihlerde araba müsait değil.')

    return render(request, 'pages/car_detail.html', {
        'car': car,
        'now': timezone.now(),
        'car_id': car.id,
        'booked_dates_json': json.dumps(booked_dates_list),
        'title': title,
    })

def blog(request):
    title = 'Blog'
    return render(request, 'pages/blog.html', {
        'title': title,
    })

def blog_detail(request, slug):
    title = 'Blog'
    return render(request, 'pages/blog_detail.html', {
        'title': title,
    })

def contact(request):
    title = 'İletişim'
    return render(request, 'pages/contact.html', {
        'title': title,
    })

def about(request):
    title = 'Hakkımızda'
    return render(request, 'pages/about.html', {
        'title': title,
    })

def myaccount(request):
    title = 'Hesabım'
    return render(request, 'pages/myaccount.html', {
        'title': title,
    })

def login(request):
    title = 'Giriş Yap'
    return render(request, 'pages/login.html', {
        'title': title,
    })

def register(request):
    title = 'Kayıt Ol'
    return render(request, 'pages/register.html', {
        'title': title,
    })





