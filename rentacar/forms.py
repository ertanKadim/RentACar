from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import User
from .models import CaseType
# from .models import Car

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class RegisterForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_customer'] = forms.BooleanField(
            initial=True, # otomatik customer olarak gelsin diye ayarladım.
            required=False,
            widget=forms.HiddenInput(),
        )

# from .models import Car

# class CarRentalForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         fields = [
#             'pickup_location', 'dropoff_location', 'start_date', 
#             'start_time', 'return_date', 'return_time'
#         ]




class CaseTypeFilterForm(forms.Form):
    case_types = forms.ModelMultipleChoiceField(
        queryset=CaseType.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'type': 'case_types'}),
        required=False,
        to_field_name='id'  # Kategori ID'lerini kullan
    )