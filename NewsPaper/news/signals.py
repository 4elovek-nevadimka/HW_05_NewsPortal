from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, created, **kwargs):
    if created:
        # пока добавляем просто первую категорию
        cat = Category.objects.get(pk=1)
        instance.categories.add(cat)
        mail_messages = []
        for subscriber in cat.subscribers.all():
            mail_messages.append(create_mail_message(instance, subscriber))

        if len(mail_messages) > 0:
            connection = mail.get_connection()
            # Manually open the connection
            connection.open()
            connection.send_messages(mail_messages)
            # We need to manually close the connection.
            connection.close()


def create_mail_message(new_post, subscriber):
    html_content = render_to_string(
        'mail_new_post_notification.html',
        {
            'post': new_post,
            'user': subscriber,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'New post: {new_post.title}',
        body=new_post.text,
        from_email='skillfactorymailserver@yandex.ru',
        to=[subscriber.email],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg
