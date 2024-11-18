from django.apps import AppConfig


class MyAccountConfig(AppConfig):
    """
    Configuration class for the 'my_account' app.
    """
    # Default field type for primary keys in the app's models
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the app
    name = 'my_account'

    def ready(self):
        """
        Override the ready method to import signals when the app is loaded.
        """
        import my_account.signals
