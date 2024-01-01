from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Car, Booking, Blog, Comment
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
import json
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, UserPasswordChangeForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.mail import send_mail


def index(request):
    title = 'Anasayfa'

    cars = list(Car.objects.order_by('-created_at')[:5])
    blogs = list(Blog.objects.order_by('-created_at')[:3])

    return render(request, 'pages/index.html', {
        'title': title,
        'cars': cars,
        'blogs': blogs,
    })


def cars(request):
    cars = Car.objects.all()

    case_type_value = request.GET.getlist('case_type')
    if case_type_value:
        cars = cars.filter(case_type__type__in=case_type_value)

    case_type_counts_query = Car.objects.values('case_type__type').annotate(count=Count('case_type'))
    case_type_counts = {item['case_type__type']: item['count'] for item in case_type_counts_query}

    # Checkbox durumlarını template'e göndermek için bir sözlük hazırlayın
    checkbox_values = {value: "checked" for value in case_type_value}

    return render(request, 'pages/cars.html', {
        'cars': cars,
        'checkbox_values': checkbox_values,
        'case_type_counts': case_type_counts
    })



@login_required
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
            current += timedelta(days=1)

    if request.method == 'POST':
        # Kullanıcının formdan gönderdiği tarihleri al
        start_date = request.POST.get('pick-up-date')
        start_time = request.POST.get('pick-up-time')
        return_date = request.POST.get('collection-date')
        return_time = request.POST.get('collection-time')
        pickup_location = request.POST.get('pickup-location')
        dropoff_location = request.POST.get('dropoff-location')

        # Session'a bilgileri kaydet
        request.session['booking_details'] = {
            'car_id': car.id,
            'start_date': start_date,
            'start_time': start_time,
            'return_date': return_date,
            'return_time': return_time,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location
        }

        request.session['payment_access_allowed'] = True
        return redirect('payment')

    return render(request, 'pages/car_detail.html', {
        'car': car,
        'now': timezone.now(),
        'booked_dates_json': json.dumps(booked_dates_list),
        'title': title,
    })

@login_required
def payment(request):
    # if request.method == 'GET' and not request.session.pop('payment_access_allowed', False):
    #     return redirect('index')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            booking_details = request.session.get('booking_details')
            if booking_details:
                start_datetime = datetime.strptime(f"{booking_details['start_date']} {booking_details['start_time']}", '%d %B %Y %H:%M')
                return_datetime = datetime.strptime(f"{booking_details['return_date']} {booking_details['return_time']}", '%d %B %Y %H:%M')

                Booking.objects.create(
                    user=request.user,
                    car_id=booking_details['car_id'],
                    start_date=start_datetime.date(),
                    start_time=start_datetime.time(),
                    return_date=return_datetime.date(),
                    return_time=return_datetime.time(),
                    pickup_location=booking_details['pickup_location'],
                    dropoff_location=booking_details['dropoff_location'],
                )
                messages.success(request, 'Ödeme başarılı. Araba başarıyla kiralandı!')
                return redirect('payment')
            else:
                messages.error(request, 'Rezervasyon detayları bulunamadı.')
        else:
            messages.error(request, 'Ödeme sırasında bir hata oluştu.')
    else:
        if 'booking_details' not in request.session:
            return redirect('index')
        
        form = PaymentForm()

    return render(request, 'pages/payment.html', {'form': form})

def blog(request):
    title = 'Blog'
    blogs = Blog.objects.all()
    blog_recent_posts = list(Blog.objects.order_by('-created_at')[:5])
    return render(request, 'pages/blog.html', {
        'title': title,
        'blogs': blogs,
        'blog_recent_posts': blog_recent_posts,
    })

def blog_detail(request, slug):
    title = 'Blog'
    blog = get_object_or_404(Blog, slug=slug)
    blog_detail_recent_posts = list(Blog.objects.order_by('-created_at')[:5])

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_content = request.POST.get('comment')
            if comment_content:
                Comment.objects.create(blog=blog, user=request.user, content=comment_content)
                return HttpResponseRedirect(request.path_info)
        else:
            return redirect('user_login')

    comments = Comment.objects.filter(blog=blog).order_by('-created_at')

    return render(request, 'pages/blog_detail.html', {
        'title': title,
        'blog': blog,
        'comments': comments,
        'blog_detail_recent_posts': blog_detail_recent_posts,
    })

def contact(request):
    title = 'İletişim'
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        send_mail(
            subject=f"Yeni İletişim Formu Mesajı - {name}",
            message=f"Mesaj: {message}\nE-posta: {email}\nTelefon: {phone}",
            from_email=email,
            recipient_list=['kadimertan78@gmail.com'],
        )

        messages.success(request, 'Mesajınız başarıyla gönderildi!')
        return redirect('contact')
    return render(request, 'pages/contact.html', {
        'title': title,
    })

def about(request):
    title = 'Hakkımızda'
    return render(request, 'pages/about.html', {
        'title': title,
    })

@login_required
def account_dashboard(request):
    title = 'Hesabım'
    bookings = Booking.objects.filter(user=request.user)  # Kullanıcının rezervasyonlarını çek
    return render(request, 'pages/account_dashboard.html', {
        'title': title,
        'bookings': bookings,
    })

@login_required
def account_profile(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect('account_profile')
        else:
            messages.error(request, form.errors)
    else:
        form = UserPasswordChangeForm(user=request.user)

    return render(request, 'pages/account_profile.html', {
        'form': form,
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
            print(errors)
            msg = 'Kayıt başarısız!'
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'form': form, 'msg': msg, 'title': title})

def user_login(request):
    title = 'Giriş Yap'
    
    if request.user.is_authenticated:
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





