from __future__ import absolute_import

import logging

from django.db              import connection

from celery                 import shared_task

from core.utils             import sayIsoDateTimeNoTimeZone, getPriorDateTime

from .models                import Keeper
from .utils                 import ( getSingleItemThenStore,
                                     getFindersForResultsFetching,
                                     getItemPictures,
                                     getItemsForPicsDownloading )

from finders.models         import ItemFound, UserItemFound


logger = logging.getLogger(__name__)

logging_level = logging.INFO


# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



@shared_task( name = 'keepers.tasks.getSingleItemThenStore' )
def doGetSingleItemThenStoreTask( iItemNumb, **kwargs ):
    #
    getSingleItemThenStore( iItemNumb, **kwargs )



@shared_task( name = 'keepers.tasks.deleteOldItemsFound' )
def deleteOldItemsFoundTask( iOldCutOff ):
    #
    # itemsfound is for temporary holding
    # AFTER ebay info is no longer available,
    # (about 90 days after auction end),
    # can delete userfinders itemsfound and useritemsfound
    #
    cursor = connection.cursor()
    #
    sPastDate = sayIsoDateTimeNoTimeZone(
                    getPriorDateTime( iDaysAgo = iOldCutOff )
    #
    sCommand = ( 'delete from userfinders where "tTimeEnd" < '
                 "'%s'" ) % sPastDate
    #
    cursor.execute( sCommand )
    #
    sCommand = ( 'delete from itemsfound where "tTimeEnd" < '
                 "'%s'" ) % sPastDate
    #
    cursor.execute( sCommand )
    #
    # now CAREFULLY delete unneeded useritemsfound rows!
    #
    sCommand = (
        '''delete from useritemsfound uif
                where not exists
                    ( select 1 from itemsfound if
                        where if."iItemNumb" = uif."iItemNumb_id" ) ;
        ''' )
    #
    cursor.execute( sCommand )
    #




@shared_task( name = 'keepers.tasks.getFetchUserItems' )
def doGetFetchUserItemsTasks( bOnlySay = False, bDoFinalOnly = False ):
    #
    qsUserItemNumbs = getFindersForResultsFetching()
    #
    if bOnlySay or bDoFinalOnly:
        #
        print( 'would fetch results on %s items now'
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
    tYesterday = getPriorDateTime( iDaysAgo = 1 )
    #
    iOldCutOff = 100
    tOldItems  = getPriorDateTime( iDaysAgo = iOldCutOff )
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
        print( 'would fetch final results on %s items now'
                % qsItemsFinal.count() )
        #
        if iOldItems:
            #
            print( 'would delete %s items older than %s days'
                    % ( iOldItems, iOldCutOff ) )
            #
        else:
            #
            print( 'no older items to delete at this moment' )
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
            # deleteOldItemsFoundTask.apply_async(
            #         queue='low_priority', args = (iOldCutOff,) )
            #
            deleteOldItemsFoundTask.delay( iOldCutOff )
            #
        #



@shared_task( name = 'keepers.tasks.getItemPictures' )
def getItemPicturesTask( iItemNumb ):
    #
    getItemPictures( iItemNumb )


@shared_task( name = 'keepers.tasks.doGetItemPicturesTasks' )
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
            oFirst = Keeper.objects.get( iItemNumb = qsGetPics[0] )
            #
            for iItemNumb in qsGetPics: iLast = iItemNumb # negative indexing not supported!
            #
            oLast = Keeper.objects.get( iItemNumb = iLast )
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


would fetch results on how many items now?

select count( DISTINCT "iItemNumb_id" )
    from useritemsfound
    where "bGetPictures" is true and  "tRetrieved" is null ;


would fetch final results on how many items now?

select count(*) from itemsfound
    where "tTimeEnd" <= current_timestamp - interval '1 day' and
    "iItemNumb" in
        ( select distinct "iItemNumb_id" from useritemsfound
            where "tRetrieved" is not null and "tRetrieveFinal" is null );

would delete how many items older than 100 days?

select count(*) from itemsfound
    where "tTimeEnd" <= current_timestamp - interval '100 days' ;



# doGetItemPicturesTasks( bOnlySay = True )

select count(*) from keepers where "tGotPictures" is null  ;
select "iItemNumb", "tTimeEnd" from keepers where "tGotPictures" is null order by "tTimeEnd" limit 1 ;

select count(*) from keepers where "iGotPictures" > 0 ;

select "cTitle", "iGotPictures" from keepers where "tGotPictures" =
    ( select max( "tGotPictures" ) from keepers ) ;

'''

# from keepers.tasks import doGetFetchUserItemsTasks, doGetItemPicturesTasks
# doGetFetchUserItemsTasks( bOnlySay = True )
# doGetFetchUserItemsTasks( bDoFinalOnly = True )
# doGetFetchUserItemsTasks()
# doGetItemPicturesTasks( bOnlySay = True )
# doGetItemPicturesTasks()
