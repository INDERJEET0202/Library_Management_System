from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

celery = Celery(__name__)

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    include=['tasks'],  
    result_expires=10
)

celery.conf.beat_schedule = {
    'send-remainder-to-inactive-members': {
        'task': 'tasks.send_remainder',
        'schedule': crontab(minute=0, hour=12), 
        # 'schedule': timedelta(minutes=1), #for checking every minute
    },
    'create-pdf-of-users': {
        'task': 'tasks.create_pdf',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),  
    },
}