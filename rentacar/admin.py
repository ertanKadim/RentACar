from django.contrib import admin
from .models import Car, Category, Booking

class CarAdmin(admin.ModelAdmin):
    list_display = ['category', 'brand', 'model', 'year', 'is_available', 'is_damaged', 'price_per_day', 'start_date', 'pickup_location', 'return_date', 'dropoff_location']
    list_filter = ['category']
    list_display_links = ['brand', 'model', 'year']

    class Meta:
        model = Car

admin.site.register(Car, CarAdmin)
admin.site.register(Category)
admin.site.register(Booking)