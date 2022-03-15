import logging
from collections import defaultdict
from datetime import timedelta, datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def weekly_mail_notification():
    dic = defaultdict(list)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    for post in Post.objects.filter(creation_date__range=[week_ago, today]):
        for category in post.categories.all():
            for subscriber in category.subscribers.all():
                dic[subscriber].append(post)
    # формирование рассылки
    mail_messages = []
    for subscriber in dic.keys():
        mail_messages.append(create_mail_message(subscriber, dic[subscriber]))

    if len(mail_messages) > 0:
        connection = mail.get_connection()
        # Manually open the connection
        connection.open()
        connection.send_messages(mail_messages)
        # We need to manually close the connection.
        connection.close()

    # debug print
    # print(dic.items())
    # for user in dic.keys():
    #     print(user.username)
    #     for post in dic[user]:
    #         print(post.title)


def create_mail_message(subscriber, weekly_posts):
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_mail_notification,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week="thu"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="weekly_mail_notification",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
