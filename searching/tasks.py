from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import Celery
from celery.schedules       import crontab
from celery                 import shared_task

from .utils                 import ( trySearchCatchExceptStoreInFile,
                                     storeSearchResultsInDB )
from .utils_stars           import findSearchHits

from .models                import Search, SearchLog, UserItemFound

from core.utils             import getBegTime, sayDuration

from String.Output          import ReadableNo


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



@shared_task( name = 'auctionbot.searching.tasks.trySearchCatchExceptStoreInFile' )
def doTrySearchCatchExceptStoreInFileTask( iSearchID ):
    #
    trySearchCatchExceptStoreInFile( iSearchID )



def doSearchingPutResultsInFiles( bOnlyList = False, bConsoleOut = False ):
    #
    # really want to select for active users only (not inactive)
    #
    tBeg = getBegTime( bConsoleOut )
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
            print( 'would do %s "%s" search for %s ...' %
                    ( oSearch.id, oSearch, oSearch.iUser.name ) )
            #
        else:
            #
            if bConsoleOut:
                #
                print( 'Doing %s "%s" search for %s ...' %
                        ( oSearch.id, oSearch, oSearch.iUser.name ) )
            #
            sLastFile = doTrySearchCatchExceptStoreInFileTask.delay(
                            iSearchID = oSearch.id ) 
            #
            if bConsoleOut:
                #
                print(
                    'Search %s "%s" for %s yielded file "%s"' %
                    ( oSearch.id, oSearch.cTitle, oSearch.iUser.name, sLastFile ) )
                print( '' )
            #
            if iSeq < iSearches: sleep( 1 )
            #
        #
    #
    if bConsoleOut:
        #
        sayDuration( tBeg )


@shared_task( name = 'auctionbot.searching.tasks.storeSearchResultsInDB' )
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




def putSearchResultsInItemsFound( bOnlyList = False, bConsoleOut = False ):
    #
    tBeg = getBegTime( bConsoleOut )
    #
    qsLogSearches = (
            SearchLog.objects.filter(
                tBegSearch__isnull = False,
                tEndSearch__isnull = False,
                tBegStore__isnull  = True,
                cResult = 'Success' ).order_by( "tBegSearch" ) )
    #
    for oLogSearch in qsLogSearches:
        #
        iLogID      = oLogSearch.pk
        iSearchID   = oLogSearch.iSearch.pk
        sSearchName = oLogSearch.iSearch.cTitle
        sUserName   = oLogSearch.iSearch.iUser.username
        sMarket     = oLogSearch.iSearch.iUser.iEbaySiteID.cMarket
        #
        if bOnlyList:
            #
            print( 'would store items from the "%s" search named %s' %
                    ( sUserName, sSearchName ) )
            #
        else:
            #
            if bConsoleOut:
                #
                print( 'Storing the items from the %s search named "%s" ...' %
                        ( sUserName, sSearchName ) )
            #
            t = storeSearchResultsInDB( iLogID,
                                        sMarket,
                                        sUserName,
                                        iSearchID,
                                        sSearchName )
            #
            iItems, iStoreItems, iStoreUsers = t
            #
            sItems      = ReadableNo( iItems      )
            sStoreItems = ReadableNo( iStoreItems )
            sStoreUsers = ReadableNo( iStoreUsers )
            #
            if bConsoleOut:
                #
                sStoreVerb = 'was' if iStoreItems == 1 else 'were'
                sUsersVerb = 'was' if iStoreUsers == 1 else 'were'
                #
                print(
                    'got %s items, of which %s %s new, '
                    'and %s %s new for %s.' %
                    ( sItems,      sStoreItems, sStoreVerb,
                      sStoreUsers, sUsersVerb,  sUserName ) )
                print( '' )
            #
    #
    if bConsoleOut:
        #
        sayDuration( tBeg )
    #


@shared_task( name = 'auctionbot.searching.tasks.findSearchHits' )
def findSearchHitsTask( iUser, bCleanUp = True, bShowProgress = False ):
    #
    print( 'calling findSearchHits() for %s now ....' % iUser )
    #
    findSearchHits( iUser,
                    bCleanUpAfterYourself   = bCleanUp,
                    bShowProgress           = bShowProgress )
    #


def doFindSearhHitsTasks( bCleanUpAfterYourself = True, bConsoleOut = False ):
    #
    oUserModel = get_user_model()
    #
    for oUser in oUserModel.objects.all():
        #
        if ( UserItemFound.objects
                        .filter( iUser = oUser.id,
                        tLook4Hits__isnull = True ).exists() ):
            #
            findSearchHitsTask.delay(
                    iUser           = oUser.id,
                    bCleanUp        = bCleanUpAfterYourself,
                    bShowProgress   = bConsoleOut )
    #


def doFindSearhHits( bCleanUpAfterYourself = True, bConsoleOut = False ):
    #
    tBeg = getBegTime( bConsoleOut )
    #
    oUserModel = get_user_model()
    #
    for oUser in oUserModel.objects.all():
        #
        if ( UserItemFound.objects
                        .filter( iUser = oUser.id,
                        tLook4Hits__isnull = True ).exists() ):
            #
            findSearchHits(
                    iUser           = oUser.id,
                    bCleanUp        = bCleanUpAfterYourself,
                    bShowProgress   = bConsoleOut )
    #
    if bConsoleOut:
        #
        sayDuration( tBeg )



def doAllUnattended():
    #
    doSearchingPutResultsInFiles( bConsoleOut = True )
    putSearchResultsInItemsFound( bConsoleOut = True )
    doFindSearhHits( bConsoleOut = True )


def doMostUnattended():
    #
    doSearchingPutResultsInFiles( bConsoleOut = True )
    putSearchResultsInItemsFound( bConsoleOut = True )
    # doFindSearhHits( bConsoleOut = True )



# workflow
# 30 mins per user doSearchingPutResultsInFiles
# 40 mins per user putSearchResultsInItemsFound
# 90 mins per user doFindSearhHits
