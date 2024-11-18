from django.apps import AppConfig


class BasketV2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket_v2'

    def ready(self):
        import basket_v2.signals
