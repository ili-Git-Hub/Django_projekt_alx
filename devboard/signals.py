from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from devboard.models import Task

def save_done_info(sender, instance, **kwargs):
    print(f"Zapisano {instance} do bazy!")

@receiver(post_save, sender=Task, dispatch_uid="save_done_info2_on_taks")
def save_done_info2(sender, instance, **kwargs):
    print(f"Zapisano {instance} do bazy!")

@receiver(pre_save, sender=Task, dispatch_uid="task_status_change_check")
def check_old_status(sender, instance, **kwargs):
    if instance.pk:
        status = sender.objects.filter(pk=instance.pk).first().status  # to można jeszcze zo
        instance._old_status = status  # uwaga, trick!

@receiver(post_save, sender=Task, dispatch_uid="task_status_change_log")
def log_status_change(sender, instance, created, **kwargs):
    if created:
        return
    if hasattr(instance, "_old_status") and (instance._old_status != instance.status):
        print(f"Task {instance.title} status changed: {instance._old_status} -> {instance.status}")