from django.apps import AppConfig

class RentacarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentacar'

    def ready(self):
        # Burada sinyal işleyicilerinizi import edin
        from . import signals
