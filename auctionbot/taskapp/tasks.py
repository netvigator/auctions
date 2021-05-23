#from celery     import shared_task

from .celery    import app

# 2021-05-24 celery not working, so giving up on it!
# instead, will set nice level on cron job processes
# will leave the celery structure in place, to allow retrying later if desired

#@shared_task( name = 'auctionbot.taskapp.tasks.add' )
def add( i, j ): return i + j


