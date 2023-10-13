from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autoslug import AutoSlugField

def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(f"{value} yılı geçerli değil. Yıl en fazla {current_year} olabilir.")


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Marka Adı")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"
        ordering = ['name']

class Series(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='series')
    name = models.CharField(max_length=100, verbose_name="Seri Adı")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Seri"
        verbose_name_plural = "Seriler"
        ordering = ['name']

# Adjust the Model class to have a ForeignKey to Series
class Model(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, related_name='models')  # Add this line
    name = models.CharField(max_length=100, verbose_name="Model Adı")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Modeller"
        ordering = ['name']


class FuelType(models.Model):
    type = models.CharField(max_length=50, verbose_name="Yakıt Türü")
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = "Yakıt Türü"
        verbose_name_plural = "Yakıt Türleri"
        ordering = ['type']

class TransmissionType(models.Model):
    type = models.CharField(max_length=50, verbose_name="Vites Türü")
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = "Vites Türü"
        verbose_name_plural = "Vites Türleri"
        ordering = ['type']

class VehicleType(models.Model):
    type = models.CharField(max_length=50, verbose_name="Araç Tipi")
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = "Araç Tipi"
        verbose_name_plural = "Araç Tipleri"
        ordering = ['type']

class CaseType(models.Model):
    type = models.CharField(max_length=50, verbose_name="Kasa Tipi")
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = "Kasa Tipi"
        verbose_name_plural = "Kasa Tipleri"
        ordering = ['type']

class Car(models.Model):
    # Kategori ve Durum Bilgileri
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Marka")
    series = models.ForeignKey(Series, on_delete=models.CASCADE, verbose_name="Seri")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name="Model")
    year = models.IntegerField(validators=[validate_year], verbose_name="Yıl")
    is_available = models.BooleanField(default=False, verbose_name="Kiralık Mı?")
    is_damaged = models.BooleanField(default=False, verbose_name="Hasarlı Mı?")

    # Teknik Özellikler
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, verbose_name="Araç Tipi")
    case_type = models.ForeignKey(CaseType, on_delete=models.SET_NULL, null=True, verbose_name="Kasa Tipi")
    km = models.IntegerField(verbose_name="Kilometre")
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name="Yakıt Türü")
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.SET_NULL, null=True, verbose_name="Vites Türü")
    number_of_doors = models.CharField(max_length=2, verbose_name="Kapı Sayısı")
    number_of_seats = models.CharField(max_length=2, null=True, verbose_name="Koltuk Sayısı")
    luggage_volume = models.CharField(max_length=50, verbose_name="Bagaj Hacmi")
    color = models.CharField(max_length=50, verbose_name="Renk")
    # number_of_person = models.CharField(max_length=2, verbose_name="Kişi Sayısı")

    # Kiralama Bilgileri
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Günlük Fiyat")
    # pickup_location = models.CharField(null=True, blank=True, max_length=255, verbose_name="Alış Yeri")
    # dropoff_location = models.CharField(null=True, blank=True, max_length=255, verbose_name="Teslim Yeri")
    # start_date = models.DateField(null=True, blank=True, verbose_name="Kiralanma Tarihi")
    # start_time = models.TimeField(null=True, blank=True, verbose_name="Kiralanma Saati")
    # return_date = models.DateField(null=True, blank=True, verbose_name="Teslim Tarihi")
    # return_time = models.TimeField(null=True, blank=True, verbose_name="Teslim Saati")

    # Görseller
    image1 = models.URLField(null=True, blank=True, verbose_name="1. Fotoğrak Linki")
    image2 = models.URLField(null=True, blank=True, verbose_name="2. Fotoğrak Linki")
    image3 = models.URLField(null=True, blank=True, verbose_name="3. Fotoğrak Linki")
    image4 = models.URLField(null=True, blank=True, verbose_name="4. Fotoğrak Linki")

    plate_number = models.CharField(max_length=10, unique=True, verbose_name="Plaka Numarası", null=True, blank=True)
    slug = AutoSlugField(populate_from='get_slug', unique=True, verbose_name="Slug")

    def get_slug(self):
        slug = f"{self.brand.name}-{self.series.name}-{self.model.name}-{self.year}-{self.id}"  # Adjusted to include series
        return slug

    def __str__(self):
        return f"{self.brand} {self.series} {self.model} ({self.year})"  # Adjusted to include series
    
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

