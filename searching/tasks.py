from django.utils       import timezone
from django.db.models   import Q

from celery             import Celery
from celery.schedules   import crontab

from .utils             import trySearchCatchExceptions
from .utils_stars       import findSearchHits

from .models            import Search

from String.Output      import ReadableNo

# trySearchCatchExceptions( iSearchID = None, sFileName = None )
# findSearchHits( oUser )

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

def doAllSearching():
    #
    # really want to select for active users only (not inactive)
    #
    tNow = timezone.now()
    tAgo = tNow - timezone.timedelta( hours = 12 )
    #
    oSearches = Search.objects.filter(
            Q( tSearchStarted__isnull = True ) or
            Q( tSearchStarted__gte    = tAgo ) ).order_by('cPriority')
    #
    for oSearch in oSearches:
        #
        print( 'Searching for %s for %s ...' %
                ( oSearch, oSearch.iUser.name ) )
        #
        t = trySearchCatchExceptions( iSearchID = oSearch.id ) 
        #
        iItems, iStoreItems, iStoreUsers = t
        #
        sItems      = ReadableNo( iItems      )
        sStoreItems = ReadableNo( iStoreItems )
        sStoreUsers = ReadableNo( iStoreUsers )
        #
        print(
            'got %s items, of which %s were new, and %s were new for %s.' %
            ( sItems, sStoreItems, sStoreUsers, oSearch.iUser.name ) )
        print( '' )
        #



