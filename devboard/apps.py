from django.apps import AppConfig
from django.db.models.signals import post_save


class DevboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devboard'
    verbose_name = 'API Devboard v.0.1' #tu wpisujemmy przyjzaną nazwe aplikacji w adminie aby bylo ladniej

    def ready(self):
        print('API Devboard została uruchomiona')   #na starcie wywolujemy komunikat :)

        # Sygnał, opcja 1:
        # from devboard.models import Task
        # post_save.connect(save_done_info, sender=Task, dispatch_uid="save_done_info_on_task")

        # Sygnał, opcja 2 - @receiver w signals.py:
        from devboard import signals  # noqa: F401
