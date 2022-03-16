from collections import defaultdict
from datetime import datetime, timedelta

from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Category, Post


def send_email_by_signal(new_post):
    cat = Category.objects.get(pk=1)    # пока добавляем просто первую категорию
    new_post.categories.add(cat)

    mail_messages = []
    for subscriber in cat.subscribers.all():
        mail_messages.append(create_one_time_mail_message(new_post, subscriber))
    send_multiple_emails(mail_messages)


def send_email_by_scheduler():
    subscribers_posts = defaultdict(list)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    for post in Post.objects.filter(creation_date__range=[week_ago, today]):
        for category in post.categories.all():
            for subscriber in category.subscribers.all():
                subscribers_posts[subscriber].append(post)

    mail_messages = []
    for subscriber in subscribers_posts.keys():
        mail_messages.append(create_weekly_mail_message(subscriber, subscribers_posts[subscriber]))
    send_multiple_emails(mail_messages)


def send_multiple_emails(mail_messages):
    if len(mail_messages) > 0:
        connection = mail.get_connection()
        connection.send_messages(mail_messages)


def create_one_time_mail_message(new_post, subscriber):
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


def create_weekly_mail_message(subscriber, weekly_posts):
    html_content = render_to_string(
        'mail_weekly_notification.html',
        {
            'weekly_posts': weekly_posts,
            'user': subscriber,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Your weekly collection of publications',
        body='some text in body',
        from_email='skillfactorymailserver@yandex.ru',
        to=[subscriber.email],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg
