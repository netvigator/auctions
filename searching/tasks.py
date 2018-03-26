
from .utils         import trySearchCatchExceptions
from .utils_stars   import findSearchHits

from .models        import Search

from String.Output  import ReadableNo

# trySearchCatchExceptions( iSearchID = None, sFileName = None )
# findSearchHits( oUser )


def doAllSearching():
    #
    # really want to select for active users only (not inactive)
    #
    oSearches = Search.objects.all()
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


