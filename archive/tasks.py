from __future__ import absolute_import

import logging

from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import shared_task
from celery.schedules       import crontab

#from auctionbot             import celery_app as app # app = Celery()

from .utils                 import getSingleItemThenStore

from searching.models       import ItemFound, UserItemFound

logger = logging.getLogger(__name__)

logging_level = logging.INFO


# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



@shared_task( name = 'archive.tasks.getSingleItemThenStore' )
def doGetSingleItemThenStoreTask( iItemNumb, **kwargs ):
    #
    getSingleItemThenStore( iItemNumb, **kwargs )



@shared_task( name = 'archive.tasks.getFetchUserItems' )
def doGetFetchUserItemsTasks( bOnlySay = False ):
    #
    qsUserItemNumbs = ( UserItemFound.objects.filter(
                                bGetPictures        = True,
                                tRetrieved__isnull  = True )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
    #
    qsAlreadyFetched = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserItemNumbs )
                            .filter( tRetrieved__isnull = False )
                            .prefetch_related(
                                    'tRetrieved', 'tRetrieveFinal' ) )
    #
    for oItemFound in qsAlreadyFetched:
        #
        qsUserItemFound = UserItemFound.filter(
                                iItemNumb = oItemFound.iItemNumb )
        #
        for oUserItemFound in qsUserItemFound:
            #
            oUserItemFound.tRetrieved     = oItemFound.tRetrieved
            oUserItemFound.tRetrieveFinal = oItemFound.tRetrieveFinal
            #
            oUserItemFound.save()
            #
        #
    #
    qsAlreadyFinal = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserItemNumbs )
                            .filter( tRetrieveFinal__isnull = False )
                            .prefetch_related( 'tRetrieveFinal' ) )
    #
    for oItemFound in qsAlreadyFinal:
        #
        qsUserItemFound = UserItemFound.filter(
                                iItemNumb = oItemFound.iItemNumb )
        #
        for oUserItemFound in qsUserItemFound:
            #
            oUserItemFound.tRetrieveFinal = oItemFound.tRetrieveFinal
            #
            oUserItemFound.save()
            #
        #
    #
    if qsAlreadyFetched.exists() or qsAlreadyFinal.exists():
        #
        # must redo query
        #
        qsUserItemNumbs = ( UserItemFound.objects.filter(
                                    bGetPictures        = True,
                                    tRetrieved__isnull  = True )
                                .values_list( 'iItemNumb', flat = True )
                                .distinct() )
        #
    #
    #
    if bOnlySay:
        #
        print( 'would fetch resuls on %s items now'
                % qsUserItemNumbs.count() )
        #
    else:
        #
        for iItemNumb in qsUserItemNumbs:
            #
            doGetSingleItemThenStoreTask.delay( iItemNumb )
            #



def getFetchFinalItems( bOnlySay = False ):
    #
    tYesterday = timezone.now() - timezone.timedelta(1)
    #
    qsItemsFinal = ItemFound.objects.filter(
                tTimeEnd__lte = tYesterday,
                pk__in = UserItemFound.objects
                    .filter(    tRetrieved__isnull      = False,
                                tRetrieveFinal__isnull  = True )
                    .values_list( 'iItemNumb', flat=True ) )
    #
    if bOnlySay:
        #
        print( 'would fetch final resuls on %s items now'
                % qsItemsFinal.count() )
        #
    else:
        #
        for oItemFound in qsItemsFinal:
            #
            # assign task
            #
            pass

# from archive.tasks import doGetSingleItemThenStoreTask
# doGetSingleItemThenStoreTask
# from archive.tasks import doGetFetchUserItemsTasks
# doGetFetchUserItemsTasks( bOnlySay = True )