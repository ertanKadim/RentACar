from django import forms
from .models import Car

class CarRentalForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'pickup_location', 'dropoff_location', 'start_date', 
            'start_time', 'return_date', 'return_time'
        ]