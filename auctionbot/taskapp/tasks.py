from celery     import shared_task
from .celery    import app


@shared_task( name = 'auctionbot.taskapp.tasks.add' )
def add( i, j ): return i + j


