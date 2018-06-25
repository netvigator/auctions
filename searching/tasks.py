from __future__ import absolute_import

from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import shared_task
from celery.schedules       import crontab

#from auctionbot             import celery_app as app # app = Celery()

from .models                import Search, SearchLog, UserItemFound

from .utils                 import ( trySearchCatchExceptStoreInFile,
                                     storeSearchResultsInDB )
from .utils_stars           import findSearchHits

from core.utils             import getBegTime

# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



@shared_task( name = 'searching.tasks.trySearchCatchExceptStoreInFile' )
def doTrySearchCatchExceptStoreInFileTask( iSearchID ):
    #
    trySearchCatchExceptStoreInFile( iSearchID )


# called as a daily (periodic) task
@shared_task( name = 'searching.tasks.doSearchingPutResultsInFiles' )
def doSearchingPutResultsInFilesTasks( bOnlyList = False ):
    #
    # really want to select for active users only (not inactive)
    #
    tBeg = getBegTime()
    #
    t12hAgo = tBeg - timezone.timedelta( hours = 12 )
    t04hAgo = tBeg - timezone.timedelta( hours =  4 )
    #
    qsSearches = (
            Search.objects.filter(
                Q( tBegSearch__isnull = True    ) |
                Q( tBegSearch__lte    = t12hAgo ) ) |
            Search.objects.filter(
                    tEndSearch__isnull= True,
                    tBegSearch__lte   = t04hAgo ) ).order_by('cPriority')
    #
    if len( qsSearches ) == 0 and bOnlyList:
        #
        print( 'no searches are due for any user !' )
        #
    #
    iSearches = len( qsSearches )
    #
    iSeq = 0
    #
    for oSearch in qsSearches:
        #
        iSeq += 1
        #
        if bOnlyList:
            #
            sSearchID = str( oSearch.id ).zfill( 2 )
            #
            print( 'would do %s "%s" search for %s ...' %
                    ( sSearchID, oSearch, oSearch.iUser.name ) )
            #
        else:
            #
            sLastFile = doTrySearchCatchExceptStoreInFileTask.delay(
                            iSearchID = oSearch.id )
            #
            if iSeq < iSearches: sleep( 1 )
            #
        #
    #


@shared_task( name = 'searching.tasks.storeSearchResultsInDB' )
def storeSearchResultsInDbTask( iLogID,
                                sMarket,
                                sUserName,
                                iSearchID,
                                sSearchName ):
    #
    t = storeSearchResultsInDB( iLogID,
                                sMarket,
                                sUserName,
                                iSearchID,
                                sSearchName )
    #


# called as a hourly (periodic) task
@shared_task( name = 'searching.tasks.doPutSearchResultsInItemsFoundTasks' )
def doPutSearchResultsInItemsFoundTasks():
    #
    qsLogSearches = (
            SearchLog.objects
                .select_related('iSearch')
                .filter(
                    tBegSearch__isnull = False,
                    tEndSearch__isnull = False,
                    tBegStore__isnull  = True,
                    cResult            = 'Success' )
                .order_by( "tBegSearch" ) )
    #
    for oLogSearch in qsLogSearches:
        #
        iLogID      = oLogSearch.pk
        iSearchID   = oLogSearch.iSearch_id
        sSearchName = oLogSearch.iSearch.cTitle
        sUserName   = oLogSearch.iSearch.iUser.username
        sMarket     = oLogSearch.iSearch.iUser.iEbaySiteID.cMarket
        #
        storeSearchResultsInDbTask.delay(
                                    iLogID,
                                    sMarket,
                                    sUserName,
                                    iSearchID,
                                    sSearchName )
        #



@shared_task( name = 'searching.tasks.findSearchHits' )
def findSearchHitsTask( iUser, bCleanUp = True, bShowProgress = False ):
    #
    if bShowProgress:
        print( 'calling findSearchHits() for user ID %s now ....' % iUser )
    #
    findSearchHits( iUser,
                    bCleanUpAfterYourself   = bCleanUp,
                    bShowProgress           = bShowProgress )
    #


# called as a hourly (periodic) task
@shared_task( name = 'searching.tasks.doFindSearhHitsTasks' )
def doFindSearhHitsTasks(
            bCleanUpAfterYourself = True,
            bConsoleOut           = False,
            bDoTask_Later         = True ):
    #
    oUserModel = get_user_model()
    #
    for oUser in oUserModel.objects.all():
        #
        if ( UserItemFound.objects
                        .filter( iUser = oUser.id,
                        tLook4Hits__isnull = True ).exists() ):
            #
            if bDoTask_Later:
                #
                findSearchHitsTask.delay(
                    iUser           = oUser.id,
                    bCleanUp        = bCleanUpAfterYourself,
                    bShowProgress   = bConsoleOut )
                #
            else:
                #
                findSearchHitsTask(
                    iUser           = oUser.id,
                    bCleanUp        = bCleanUpAfterYourself,
                    bShowProgress   = bConsoleOut )
                #
            #
    #




def doAllUnattended(): # example only!
    #
    doSearchingPutResultsInFiles( bOnlyList = True )
    doPutSearchResultsInItemsFoundTasks()
    doFindSearhHitsTasks( bConsoleOut = True )





# workflow
# 30 mins per user doSearchingPutResultsInFiles
# 40 mins per user putSearchResultsInItemsFound
# 90 mins per user doFindSearhHits
# from searching.tasks import doSearchingPutResultsInFilesTasks, doPutSearchResultsInItemsFoundTasks, doFindSearhHitsTasks
