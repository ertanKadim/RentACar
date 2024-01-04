from django.contrib import admin
from .models import Car, Booking, Brand, Series, Model, FuelType, TransmissionType, CaseType, VehicleType, User, Blog, Comment

admin.site.site_header = 'Rent A Car Yönetim Paneli'

class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'series', 'model', 'year', 'is_available', 'is_damaged', 'plate_number']
    list_display_links = ['brand', 'model', 'year']

    class Meta:
        model = Car

admin.site.register(Car, CarAdmin)
admin.site.register(Brand)
admin.site.register(Series)
admin.site.register(Model)
admin.site.register(FuelType)
admin.site.register(TransmissionType)
admin.site.register(VehicleType)
admin.site.register(CaseType)
admin.site.register(Comment)

admin.site.register(User)

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_display_links = ['title', 'created_at', 'updated_at']

    class Meta:
        model = Blog

admin.site.register(Blog, BlogAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ['orderid', 'car_with_plate_number', 'start_date', 'return_date', 'status']
    list_display_links = ['orderid', 'car_with_plate_number', 'start_date', 'return_date', 'status']

    def car_with_plate_number(self, obj):
        return f"{obj.car} - {obj.car.plate_number}"
    car_with_plate_number.short_description = 'Araç - Plaka'

    class Meta:
        model = Booking

admin.site.register(Booking, BookingAdmin)