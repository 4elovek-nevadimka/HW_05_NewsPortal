from celery import shared_task

from .mail_manager import send_email_by_signal, send_email_by_scheduler
from .models import Post


@shared_task
def new_post_mail_notification(new_post_id):
    send_email_by_signal(Post.objects.get(pk=new_post_id))
    print("new post notification have been sent...")


@shared_task()
def weekly_mail_notification():
    send_email_by_scheduler()
    print("weekly notification have been sent from celery...")
