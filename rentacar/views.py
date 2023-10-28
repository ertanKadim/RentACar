from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking
from django.utils import timezone
from django.contrib import messages
import datetime
import json
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm

def index(request):
    title = 'Anasayfa'

    cars = list(Car.objects.order_by('-created_at')[:5])

    return render(request, 'pages/index.html', {
        'title': title,
        'cars': cars,
    })

def cars(request):
    title = 'Kiralık Araçlar'
    cars = Car.objects.all()  # Tüm araçları başlangıçta alın
    selected_filters = []  # Seçilen filtreleri saklamak için bir liste

    if request.method == "GET":
        if 'sedan' in request.GET:
            cars = cars.filter(case_type__type="Sedan")
            selected_filters.append("sedan")

        if 'hatchback' in request.GET:
            cars = cars.filter(case_type__type="Hatchback")
            selected_filters.append("hatchback")

        if 'suv' in request.GET:
            cars = cars.filter(case_type__type="SUV")
            selected_filters.append("suv")

        if 'pickup' in request.GET:
            cars = cars.filter(case_type__type="Pickup")
            selected_filters.append("pickup")

        if 'coupe' in request.GET:
            cars = cars.filter(case_type__type="Coupe")
            selected_filters.append("coupe")

        if 'cabrio' in request.GET:
            cars = cars.filter(case_type__type="Cabrio")
            selected_filters.append("cabrio")

        if 'station_wagon' in request.GET:
            cars = cars.filter(case_type__type="Station Wagon")
            selected_filters.append("station_wagon")

        if 'minivan' in request.GET:
            cars = cars.filter(case_type__type="Minivan")
            selected_filters.append("minivan")

        if 'sport' in request.GET:
            cars = cars.filter(case_type__type="Sport")
            selected_filters.append("sport")

    return render(request, 'pages/cars.html', {
        'title': title,
        'cars': cars,
        'selected_filters': selected_filters,  # Seçilen filtreleri şablona iletiyoruz
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

def my_account(request):
    title = 'Hesabım'
    return render(request, 'pages/myaccount.html', {
        'title': title,
    })

def register(request):
    title = 'Kayıt Ol'
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Kayıt başarılı!'
            return redirect('user_login')
        else:
            errors = form.errors
            print(errors)  # Bu satır hataları konsola yazdırır
            msg = 'Kayıt başarısız!'
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'form': form, 'msg': msg, 'title': title})

def user_login(request):
    title = 'Giriş Yap'
    
    if request.user.is_authenticated:
        # Kullanıcı zaten giriş yapmışsa, istediğiniz sayfaya yönlendirin
        if request.user.is_customer:
            return redirect('index')
        elif request.user.is_admin:
            # return redirect('admin:index')
            return redirect('index')
    
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_customer:  # Normal kullanıcı
                    return redirect('index')
                elif user.is_admin:  # Admin kullanıcı
                    return redirect('admin:index')
                    # return redirect('index')
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
        else:
            msg = 'Hatalı form!'
    
    return render(request, 'pages/login.html', {'form': form, 'msg': msg, 'title': title})


def user_logout(request):
    logout(request)
    return redirect('index')





