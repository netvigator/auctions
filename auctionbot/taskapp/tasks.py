from celery     import shared_task
from .celery    import app


@shared_task
def add( i, j ): return i + j


# https://stackoverflow.com/questions/46530784/make-django-test-case-database-visible-to-celery/46564964#46564964

@app.task(name='celery.ping')
def ping():
    # type: () -> str
    """Simple task that just returns 'pong'."""
    return 'pong'