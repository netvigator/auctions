import logging

from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import Celery
from celery.schedules       import crontab



logger = logging.getLogger(__name__)

logging_level = logging.INFO

app = Celery()

# task basics
#
# If you’re using Django ... 
# then you probably want to use the shared_task() decorator:
#   @shared_task
#   def add(x, y):
#       return x + y
# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html




def getFetchUserItems():
    #
    qsUserItemNumbs = ( UserItemFound.objects.filter(
                                bGetPictures        = True,
                                tRetrieved__isnull  = True )
                            .values('iItemNumb').distinct() )
    #
    for iItemNumb in qsUserItemNumbs:
        #
        # assign task
        #
        pass



def getFetchFinalItems():
    #
    tYesterday = timezone.now() - timedelta(1)
    #
    qsItemsFinal = ItemFound.objects.filter(
                tTimeEnd__lte = tYesterday,
                pk__in = UserItemFound.objects
                    .filter(    tRetrieved__isnull      = False,
                                tRetrieveFinal__isnull  = True )
                    .values_list( 'iItemNumb', flat=True ) )
    #
    for oItemFound in qsItemsFinal:
        #
        # assign task
        #
        pass
