from celery_factory import celery

@celery.task
def add(x, y):
    print(f"Running task: {x} + {y}")
    return x + y