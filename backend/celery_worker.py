from celery import Celery
from celery.schedules import crontab
from app import create_app


def make_celery(app):
    celery = Celery(app.import_name)

    
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    celery.conf.beat_schedule = {
        'daily-reminder': {
            'task': 'tasks.reminders.daily_reminder',
            'schedule': crontab(hour=8, minute=0),  
        },
        'monthly-report': {
            'task': 'tasks.reports.monthly_report',
            'schedule': crontab(day_of_month=1, hour=8),
        },
    }

    celery.conf.timezone = 'Asia/Kolkata'

    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app()
celery = make_celery(flask_app)


import tasks.reminders
import tasks.reports
import tasks.exports
