from django.contrib import admin
from .models import Car, Booking, Brand, Series, Model, FuelType, TransmissionType, CaseType, VehicleType

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


class BookingAdmin(admin.ModelAdmin):
    list_display = ['car_with_plate_number', 'start_date', 'return_date']
    list_display_links = ['car_with_plate_number', 'start_date', 'return_date']

    def car_with_plate_number(self, obj):
        return f"{obj.car} - {obj.car.plate_number}"
    car_with_plate_number.short_description = 'Araç - Plaka'

    class Meta:
        model = Booking

admin.site.register(Booking, BookingAdmin)