from time                   import sleep

from django.contrib.auth    import get_user_model
from django.db.models       import Q
from django.utils           import timezone

from celery                 import Celery
from celery.schedules       import crontab

from .utils                 import ( trySearchCatchExceptStoreInFile,
                                     storeSearchResultsInDB )
from .utils_stars           import findSearchHits

from .models                import Search, SearchLog

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



def doSearchingPutResultsInFiles( bOnlyList = False ):
    #
    # really want to select for active users only (not inactive)
    #
    tNow    = timezone.now()
    t12hAgo = tNow - timezone.timedelta( hours = 12 )
    t04hAgo = tNow - timezone.timedelta( hours =  4 )
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
            print( 'would do the "%s" search for %s ...' %
                    ( oSearch, oSearch.iUser.name ) )
            #
        else:
            #
            print( 'Doing the "%s" search for %s ...' %
                    ( oSearch, oSearch.iUser.name ) )
            #
            sLastFile = trySearchCatchExceptStoreInFile( iSearchID = oSearch.id ) 
            #
            print(
                'Search "%s" for %s yielded file "%s"' %
                ( oSearch.cTitle, oSearch.iUser.name, sLastFile ) )
            print( '' )
            #
            if iSeq < iSearches: sleep( 1 )
            #



def putSearchResultsInItemsFound( bOnlyList = False ):
    #
    print( 'Beg:', str( timezone.now() )[:19] )
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
            print(
                'got %s items, of which %s were new, and %s were new for %s.' %
                ( sItems, sStoreItems, sStoreUsers, sUserName ) )
            print( '' )
            #
    #
    print( 'End:', str( timezone.now() )[:19] )
    #
        
def doFindSearhHits( bCleanUpAfterYourself = True, bShowProgress = False ):
    #
    print( 'Beg:', str( timezone.now() )[:19] )
    #
    oUserModel = get_user_model()
    #
    for oUser in oUserModel.objects.all():
        #
        findSearchHits( iUser                   = oUser.id,
                        bCleanUpAfterYourself   = bCleanUpAfterYourself,
                        bShowProgress           = bShowProgress )
    #
    print( 'End:', str( timezone.now() )[:19] )
    #

# workflow
# 2 hours per user doSearchingPutResultsInFiles
# 12 mins per user putSearchResultsInItemsFound
# ??      per user doFindSearhHits redoing all, must assess normal load later
