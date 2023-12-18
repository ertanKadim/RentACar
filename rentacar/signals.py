from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Car, Booking
from django.utils import timezone

@receiver(post_save, sender=Car)
def send_damage_notification(sender, instance, **kwargs):
    if instance.is_damaged:
        # Hasarlı aracın rezervasyonlarını bul
        bookings = Booking.objects.filter(car=instance, return_date__gte=timezone.now())
        for booking in bookings:
            # Kullanıcıya e-posta gönder
            send_mail(
                'Araç Hasar Bilgisi',
                'Sevgili müşterimiz, kiraladığınız araçta bir hasar meydana geldi ve '
                'rezervasyonunuz iptal edildi. Ücret iadesi yapılacaktır.',
                'kadimertan78@gmail.com',  # Gönderenin e-posta adresi
                [booking.user.email],  # Alıcının e-posta adresi
                fail_silently=False,
            )
