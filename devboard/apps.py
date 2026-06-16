from django.apps import AppConfig


class DevboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devboard'
    verbose_name = 'API Devboard v.0.1' #tu wpisujemmy przyjzaną nazwe aplikacji w adminie aby bylo ladniej

    def ready(self):
        print('API Devboard została uruchomiona')   #na starcie wywolujemy komunikat :)
