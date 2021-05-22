from __future__ import absolute_import

from os                     import walk
from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import shared_task
from celery.schedules       import crontab

#from auctionbot             import celery_app as app # app = Celery()

from searching              import SEARCH_FILES_ROOT

from .models                import Search, SearchLog

from .utils                 import ( trySearchCatchExceptStoreInFile,
                                     storeSearchResultsInFinders )
from .utils_stars           import findSearchHits

from finders.models         import UserItemFound

from core.utils             import getBegTime

from pyPks.Dir.Get          import getMakeDir
from pyPks.Time.Output      import getIsoDate

# schedule tasks
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



# @shared_task( name = 'searching.tasks.trySearchCatchExceptStoreInFile' )
def doTrySearchCatchExceptStoreInFileTask( iSearchID, sToday ):
    #
    trySearchCatchExceptStoreInFile( iSearchID, sToday )


# called as a daily (periodic) task
# @shared_task( name = 'searching.tasks.doSearchingPutResultsInFiles' )
def doSearchingPutResultsInFilesTasks( bOnlyList = False ):
    #
    # really want to select for active users only (not inactive)
    #
    sToday = getIsoDate()
    #
    getMakeDir( SEARCH_FILES_ROOT, sToday )
    #
    tBeg = getBegTime( bOnlyList )
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
    if len( qsSearches ) > 0:
        #
        # here walk( ITEM_PICS_ROOT )
        pass
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
            # sLastFile = doTrySearchCatchExceptStoreInFileTask.delay(
            sLastFile = doTrySearchCatchExceptStoreInFileTask(
                            iSearchID   = oSearch.id,
                            sToday      = sToday )
            #
            if iSeq < iSearches: sleep( 1 )
            #
        #
    #


# @shared_task( name = 'searching.tasks.storeSearchResultsInFinders' )
def storeSearchResultsInDbTask( iLogID,
                                sMarket,
                                sUserName,
                                iSearchID,
                                sSearchName,
                                sStoreDir ):
    #
    t = storeSearchResultsInFinders(
            iLogID,
            sMarket,
            sUserName,
            iSearchID,
            sSearchName,
            sStoreDir )
    #


# called as a hourly (periodic) task
# @shared_task( name = 'searching.tasks.doPutSearchResultsInFindersTasks' )
def doPutSearchResultsInFindersTasks( bOnlySay = False ):
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
    if bOnlySay:
        #
        print( 'would put results from %s searhes into finders' %
                len( qsLogSearches ) )
        #
    else:
        #
        for oLogSearch in qsLogSearches:
            #
            iLogID      = oLogSearch.pk
            iSearchID   = oLogSearch.iSearch_id
            sSearchName = oLogSearch.iSearch.cTitle
            sUserName   = oLogSearch.iSearch.iUser.username
            sMarket     = oLogSearch.iSearch.iUser.iEbaySiteID.cMarket
            sStoreDir   = oLogSearch.cStoreDir
            #
            # storeSearchResultsInDbTask.delay(
            storeSearchResultsInDbTask(
                        iLogID,
                        sMarket,
                        sUserName,
                        iSearchID,
                        sSearchName,
                        sStoreDir )
            #



@shared_task( name = 'searching.tasks.findSearchHits' )
def findSearchHitsTask( iUser, bCleanUp = True, bShowProgress = False ):
    #
    if bShowProgress:
        print( 'calling findSearchHits() for user ID %s now ....' % iUser )
    #
    findSearchHits( iUser )
    #


# called as a hourly (periodic) task
@shared_task( name = 'searching.tasks.doFindSearhHitsTasks' )
def doFindSearhHitsTasks(
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
                    bShowProgress   = bConsoleOut )
                #
            else:
                #
                findSearchHitsTask(
                    iUser           = oUser.id,
                    bShowProgress   = bConsoleOut )
                #
            #
    #



'''
doSearchingPutResultsInFilesTasks() does NOT update database, only writes files
watch file directory SEARCH_FILES_ROOT and sort by date, most recent on top

select id, "cTitle", date_trunc('second',"tBegSearch"), date_trunc('second',"tEndSearch"), "iUser_id" from searching ;
select id, "cTitle", date_trunc('second',"tBegSearch"), date_trunc('second',"tEndSearch"), "cLastResult" from searching where "iUser_id" = 1 ;

doPutSearchResultsInFindersTasks()
select count(*) from useritemsfound where "tLook4Hits" is null ;
count should be zero at start, increase as process runs, then max out

doFindSearhHitsTasks()
select count(*) from useritemsfound where "tLook4Hits" is null ;
count should decline to zero

'''


# workflow
# 30 mins per user doSearchingPutResultsInFilesTasks
#                  doSearchingPutResultsInFilesTasks( bOnlyList = True )
# 40 mins per user putSearchResultsInFinders
# 90 mins per user doFindSearhHits
# from searching.tasks import doSearchingPutResultsInFilesTasks, doPutSearchResultsInFindersTasks, doFindSearhHitsTasks
