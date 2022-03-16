from django.db.models.signals import post_save
from django.dispatch import receiver

from .mail_manager import send_email_by_signal
from .models import Post


@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        send_email_by_signal(instance)
