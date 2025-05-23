from django.apps import AppConfig
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Remplacez 'app' par le nom exact de votre application

    def ready(self):
        import app.signals
        