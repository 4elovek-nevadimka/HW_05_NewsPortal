from django.db.models.signals import post_save
from django.dispatch import receiver

from .mail_manager import send_email_by_signal
from .models import Post
from .tasks import new_post_mail_notification


@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        # send_email_by_signal(instance)
        new_post_mail_notification.delay(instance.id)
        # new_post_mail_notification.apply_async(instance.id)
