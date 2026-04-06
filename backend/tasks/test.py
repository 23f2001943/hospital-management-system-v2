from celery_app import celery_app

@celery_app.task
def add(x, y):
    print(f"Running task: {x} + {y}")
    return x + y