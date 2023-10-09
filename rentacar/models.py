from django.db import models
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = AutoSlugField(populate_from='name', unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

class Car(models.Model):
    # Temel Bilgiler
    brand = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    year = models.IntegerField(verbose_name="Yıl")
    slug = AutoSlugField(populate_from='get_slug', unique=True, verbose_name="Slug")

    # Kategori ve Durum Bilgileri
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori")
    is_available = models.BooleanField(default=False, verbose_name="Kiralık Mı?")
    is_damaged = models.BooleanField(default=False, verbose_name="Hasarlı Mı?")

    # Teknik Özellikler
    km = models.IntegerField(verbose_name="Kilometre")
    number_of_doors = models.CharField(max_length=2, verbose_name="Kapı Sayısı")
    luggage_volume = models.CharField(max_length=50, verbose_name="Bagaj Hacmi")
    fuel_type = models.CharField(max_length=50, verbose_name="Yakıt Türü")
    transmission_type = models.CharField(max_length=50, verbose_name="Vites Türü")
    color = models.CharField(max_length=50, verbose_name="Renk")
    number_of_person = models.CharField(max_length=2, verbose_name="Kişi Sayısı")

    # Kiralama Bilgileri
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Günlük Fiyat")
    pickup_location = models.CharField(null=True, blank=True, max_length=255, verbose_name="Alış Yeri")
    dropoff_location = models.CharField(null=True, blank=True, max_length=255, verbose_name="Teslim Yeri")
    start_date = models.DateField(null=True, blank=True, verbose_name="Kiralanma Tarihi")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Kiralanma Saati")
    return_date = models.DateField(null=True, blank=True, verbose_name="Teslim Tarihi")
    return_time = models.TimeField(null=True, blank=True, verbose_name="Teslim Saati")

    # Görseller
    image1 = models.URLField(null=True, blank=True, verbose_name="1. Fotoğrak Linki")
    image2 = models.URLField(null=True, blank=True, verbose_name="2. Fotoğrak Linki")
    image3 = models.URLField(null=True, blank=True, verbose_name="3. Fotoğrak Linki")
    image4 = models.URLField(null=True, blank=True, verbose_name="4. Fotoğrak Linki")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def get_slug(self):
        slug = f"{self.brand}-{self.model}-{self.year}"
        car = Car.objects.filter(slug=slug).first()
        if car:
            slug = f"{slug}-{self.id}"
        return slug
    
    class Meta:
        verbose_name = "Araba"
        verbose_name_plural = "Arabalar"
        ordering = ['-id']

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, verbose_name="Alış Tarihi")
    start_time = models.TimeField(blank=True, verbose_name="Alış Saati")
    return_date = models.DateField(blank=True, verbose_name="Teslim Tarihi")
    return_time = models.TimeField(blank=True, verbose_name="Teslim Saati")
    pickup_location = models.CharField(blank=True, max_length=255, verbose_name="Alış Yeri")
    dropoff_location = models.CharField(blank=True, max_length=255, verbose_name="Teslim Yeri")

    @classmethod
    def is_car_available(cls, car, start_date, return_date): # end_date yerine return_date
        overlapping_bookings = cls.objects.filter(
            car=car,
            start_date__lte=return_date,
            return_date__gte=start_date # end_date__gte yerine return_date__gte
        ).exists()
        return not overlapping_bookings


    def __str__(self):
        return f"Rezervasyon - {self.car} - {self.start_date} {self.start_time} - {self.return_date} {self.return_time}"
    
    class Meta:
        verbose_name = "Rezervasyon"
        verbose_name_plural = "Rezervasyonlar"
        ordering = ['-id']
