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
admin.site.register(Booking)