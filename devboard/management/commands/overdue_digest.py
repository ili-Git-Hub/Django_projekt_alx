from django.core.management.base import BaseCommand

from devboard.models import Task

class Command(BaseCommand):
    help = "Wypisuje przeterminowane zadania"

    def handle(self, *args, **options):
        overdue = Task.objects.overdue()
        for task in overdue:
            print(self.style.WARNING(f"{task.pk}: {task.title} (termin {task.due_date})"))
        print(self.style.SUCCESS(f"Razem: {overdue.count()}"))
