from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .management.commands.send_mailings import Command as SendMailingsCommand


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Запускать каждые 5 минут
    scheduler.add_job(
        SendMailingsCommand().handle,
        'interval',
        minutes=5,
        id='send_mailings',
        replace_existing=True,
    )

    scheduler.start()