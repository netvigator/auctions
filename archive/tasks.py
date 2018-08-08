from __future__ import absolute_import

import logging

from datetime               import timedelta
from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db              import connection
from django.db.models       import Q
from django.utils           import timezone

from celery                 import shared_task
from celery.schedules       import crontab

#from auctionbot             import celery_app as app # app = Celery()

from core.utils             import sayIsoDateTimeNoTimeZone

from .models                import Item
from .utils                 import ( getSingleItemThenStore,
                                     getItemsFoundForUpdate,
                                     getItemPictures,
                                     getItemsForPicsDownloading )

from searching.models       import ItemFound, UserItemFound

logger = logging.getLogger(__name__)

logging_level = logging.INFO


# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



@shared_task( name = 'archive.tasks.getSingleItemThenStore' )
def doGetSingleItemThenStoreTask( iItemNumb, **kwargs ):
    #
    getSingleItemThenStore( iItemNumb, **kwargs )



@shared_task( name = 'archive.tasks.deleteOldItemsFound' )
def deleteOldItemsFoundTask( iOldCutOff ):
    #
    cursor = connection.cursor()
    #
    sCommand = ( 'delete from itemsfound where "tTimeEnd" < '
                 "now() - interval '%s days'" ) % iOldCutOff
    #
    cursor.execute( sCommand )
    #




@shared_task( name = 'archive.tasks.getFetchUserItems' )
def doGetFetchUserItemsTasks( bOnlySay = False, bDoFinalOnly = False ):
    #
    qsUserItemNumbs = getItemsFoundForUpdate()
    #
    if bOnlySay or bDoFinalOnly:
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
    #
    # carry on, fetch final results
    #
    tYesterday = timezone.now() - timezone.timedelta( 1 )
    #
    iOldCutOff = 100
    tOldItems  = timezone.now() - timezone.timedelta( iOldCutOff )
    #
    qsItemsFinal = ItemFound.objects.filter(
                tTimeEnd__lte = tYesterday,
                pk__in = UserItemFound.objects
                    .filter(    tRetrieved__isnull      = False,
                                tRetrieveFinal__isnull  = True )
                    .values_list( 'iItemNumb', flat = True ) )
    #
    iOldItems = ItemFound.objects.filter(
                tTimeEnd__lte = tOldItems ).count()
    #
    if bOnlySay:
        #
        print( 'would fetch final resuls on %s items now'
                % qsItemsFinal.count() )
        #
        if iOldItems:
            #
            print( 'would delete %s items older than %s days'
                    % ( iOldItems, iOldCutOff ) )
            #
        #
    else:
        #
        for oItemFound in qsItemsFinal:
            #
            # assign task
            #
            doGetSingleItemThenStoreTask.delay( oItemFound.iItemNumb )
            #
        #
        if iOldItems:
            #
            deleteOldItemsFoundTask.delay( iOldCutOff )
            #
        #



@shared_task( name = 'archive.tasks.getItemPictures' )
def getItemPicturesTask( iItemNumb ):
    #
    getItemPictures( iItemNumb )


@shared_task( name = 'archive.tasks.doGetItemPicturesTasks' )
def doGetItemPicturesTasks( iLimit = 500,  bOnlySay = False ):
    #
    qsGetPics = getItemsForPicsDownloading( iLimit )
    #
    if bOnlySay:
        #
        print( 'would fetch pictures for %s items now'
                % qsGetPics.count() )
        #
        if qsGetPics:
            #
            oFirst = Item.objects.get( iItemNumb = qsGetPics[0] )
            #
            for iItemNumb in qsGetPics: iLast = iItemNumb # negative indexing not supported!
            #
            oLast = Item.objects.get( iItemNumb = iLast )
            #
            print( 'items ending from %s to %s' %
                    ( sayIsoDateTimeNoTimeZone( oFirst.tTimeEnd ),
                      sayIsoDateTimeNoTimeZone( oLast.tTimeEnd  ) ) )
            #
        #
    else:
        #
        for iItemNumb in qsGetPics:
            #
            getItemPicturesTask.delay( iItemNumb )
            #
        #
    #


'''
doGetFetchUserItemsTasks( bOnlySay = True )

select count(*) from useritemsfound
    where "bGetPictures" = true and "tRetrieved" is null ;

#### above count depends on items selected for downloading ###

select count(*) from itemsfound
    where "tTimeEnd" < timestamp 'yesterday' and
    "iItemNumb" in
        ( select "iItemNumb_id" from useritemsfound
          where "tRetrieved" is not null and "tRetrieveFinal" is null ) ;

# doGetItemPicturesTasks( bOnlySay = True )

select count(*) from items where "iGotPictures" > 0 ;
select count(*) from items where "tGotPictures" is null  ;
select "iItemNumb", "tTimeEnd" from items where "tGotPictures" is null order by "tTimeEnd" ;


select "cTitle", "iGotPictures" from items where "tGotPictures" =
    ( select max( "tGotPictures" ) from items ) ;

'''

# from archive.tasks import doGetFetchUserItemsTasks, doGetItemPicturesTasks
# doGetFetchUserItemsTasks( bOnlySay = True )
# doGetFetchUserItemsTasks( bDoFinalOnly = True )
# doGetFetchUserItemsTasks()
# doGetItemPicturesTasks( bOnlySay = True )
# doGetItemPicturesTasks()
