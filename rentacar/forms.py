from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

# from .models import Car

class LoginForm(forms.Form):
    captcha = CaptchaField()
    
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
    captcha = CaptchaField()
    name = forms.CharField(
        label='Ad Soyad',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    username = forms.CharField(
        label='Kullanıcı Adı',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='Şifre (Tekrar)',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.CharField(
        label='E-posta',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    phone = PhoneNumberField(
        label='Telefon (+90XXXXXXXXXX)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'phone', 'captcha']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_customer'] = forms.BooleanField(
            initial=True, # otomatik customer olarak gelsin diye ayarladım.
            required=False,
            widget=forms.HiddenInput(),
        )

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        # Form alanlarını özelleştirebilirsiniz
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Eski Şifre'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni Şifre'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni Şifre (Tekrar)'})

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, widget=forms.TextInput(attrs={'placeholder': 'Kredi Kartı Numarası', 'class': 'form-control'}), label='Kredi Kartı Numarası')
    card_expiry = forms.CharField(max_length=5, min_length=5, widget=forms.TextInput(attrs={'placeholder': 'AA/YY', 'class': 'form-control'}), label='Son Kullanma Tarihi')
    card_cvv = forms.CharField(max_length=3, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'CVV', 'class': 'form-control'}), label='CVV Kodu')

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValidationError("Kredi kartı numarası 16 haneli bir sayı olmalıdır.")
        return card_number

    def clean_card_cvv(self):
        card_cvv = self.cleaned_data['card_cvv']
        if len(card_cvv) != 3 or not card_cvv.isdigit():
            raise ValidationError("CVV kodu 3 haneli bir sayı olmalıdır.")
        return card_cvv
    
# from .models import Car

# class CarRentalForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         fields = [
#             'pickup_location', 'dropoff_location', 'start_date', 
#             'start_time', 'return_date', 'return_time'
#         ]
