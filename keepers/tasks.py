from __future__ import absolute_import

import logging

from django.core.wsgi       import get_wsgi_application
from django.db              import connection

#from celery                import shared_task

from core.ebay_api_calls    import getApplicationToken
from core.utils             import sayIsoDateTimeNoTimeZone, getPriorDateTime

from .models                import Keeper
from .utils                 import ( getSingleItemThenStore,
                                     getFindersForResultsFetching,
                                     getItemPictures,
                                     getItemsForPicsDownloading )

from finders.models         import ItemFound, UserItemFound


logger = logging.getLogger(__name__)

logging_level = logging.INFO

application = get_wsgi_application()

# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

# 2021-05-24 celery not working, so giving up on it!
# instead, will set nice level on cron job processes
# will leave the celery structure in place, to allow retrying later if desired

# noted on 2021-06-23: pictures have not been downloading sice 2021-05-24 !!!

# @shared_task( name = 'keepers.tasks.getSingleItemThenStore' )
def doGetSingleItemThenStoreTask( iItemNumb, oAuthToken = None, **kwargs ):
    #
    getSingleItemThenStore( iItemNumb, oAuthToken = oAuthToken, **kwargs )



# @shared_task( name = 'keepers.tasks.deleteOldItemsFound' )
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
                    getPriorDateTime( iDaysAgo = iOldCutOff ) )
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




# @shared_task( name = 'keepers.tasks.getFetchUserItems' )
def doGetFetchUserItemsTasks(
            oAuthToken = None, bOnlySay = False, bDoFinalOnly = False ):
    #
    if oAuthToken is None:
        #
        oAuthToken = getApplicationToken()
        #
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
            # doGetSingleItemThenStoreTask.delay( iItemNumb )
            doGetSingleItemThenStoreTask( iItemNumb, oAuthToken = oAuthToken )
            #
    #
    # carry on, fetch final results
    #
    tYesterday = getPriorDateTime( iDaysAgo = 1 )
    #
    iOldCutOff = 90
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
            # doGetSingleItemThenStoreTask.delay( oItemFound.iItemNumb )
            doGetSingleItemThenStoreTask(
                    oItemFound.iItemNumb, oAuthToken = oAuthToken )
            #
        #
        if iOldItems:
            #
            # deleteOldItemsFoundTask.apply_async(
            #         queue='low_priority', args = (iOldCutOff,) )
            #
            # deleteOldItemsFoundTask.delay( iOldCutOff )
            deleteOldItemsFoundTask( iOldCutOff )
            #
        #



# @shared_task( name = 'keepers.tasks.getItemPictures' )
def getItemPicturesTask( iItemNumb ):
    #
    getItemPictures( iItemNumb )


# @shared_task( name = 'keepers.tasks.doGetItemPicturesTasks' )
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
            qsGetDates = Keeper.objects.filter(
                    iItemNumb__in = qsGetPics
                    ).order_by( 'tTimeEnd'
                    ).values_list( 'tTimeEnd', flat = True
                    )
            dFirst = qsGetDates[0]
            #
            for d in qsGetDates: dLast = d # negative indexing not supported!
            #
            print( 'items ending from %s to %s' %
                    ( sayIsoDateTimeNoTimeZone( dFirst ),
                      sayIsoDateTimeNoTimeZone( dLast  ) ) )
            #
        #
    else:
        #
        try:
            #
            for iItemNumb in qsGetPics:
                #
                # getItemPicturesTask.delay( iItemNumb )
                getItemPicturesTask( iItemNumb )
                #
            #
        except PermissionError:
            #
            # problem with permissions in pictures directory
            # no need to keep trying until problem is solved!
            #
            raise
            #
        #
    #


'''
doGetFetchUserItemsTasks( bOnlySay = True )


would fetch results on how many items now?

select count( DISTINCT "iItemNumb_id" )
    from useritemsfound
    where "bGetResult" is true and  "tRetrieved" is null ;


would fetch final results on how many items now?

select count(*) from itemsfound
    where "tTimeEnd" <= current_timestamp - interval '1 day' and
    "iItemNumb" in
        ( select distinct "iItemNumb_id" from useritemsfound
            where "tRetrieved" is not null and "tRetrieveFinal" is null );

would delete how many items older than 90 days?

select count(*) from itemsfound
    where "tTimeEnd" < current_timestamp - interval '90 days' ;



# doGetItemPicturesTasks( bOnlySay = True )

select count(*) from keepers where "tGotPictures" is null and "iBidCount" > 0 ;

select "iItemNumb", "tTimeEnd" from keepers
    where "tGotPictures" is null and "iBidCount" > 0
    order by "tTimeEnd" limit 1 ;

select count(*) from keepers where "iGotPictures" > 0 ;

select "cTitle", "iGotPictures" from keepers where "tGotPictures" =
    ( select max( "tGotPictures" ) from keepers ) ;

'''

# from keepers.tasks import doGetFetchUserItemsTasks, doGetItemPicturesTasks
# from keepers.tasks import doGetItemPicturesTasks
# doGetFetchUserItemsTasks( bOnlySay = True )
# doGetFetchUserItemsTasks( bDoFinalOnly = True )
# doGetFetchUserItemsTasks()
# doGetItemPicturesTasks( bOnlySay = True )
# doGetItemPicturesTasks()
