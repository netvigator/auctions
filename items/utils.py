from json       import load

from Dict.Get   import getAnyKey

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass


def getSearchResults( sFile ):
    #
    dResults = load( open( sFile ) )
    #
    # findItemsAdvancedResponse
    # findItemsByCategoryResponse
    # findItemsByKeywordsResponse
    #
    sTopKey = getAnyKey( dResults )
    #
    dResponse = dResults[ sTopKey ]
    #
    if dResponse[ "ack" ] != "Success":
        #
        sMessage = 'ack returned "%s"' % dResponse[ "ack" ]
        #
        raise SearchNotWorkingError( sMessage )
        #
    #
    dPagination = dResponse[ "paginationOutput" ]
    #
    iEntries    = int( dPagination[ "totalEntries" ] )
    #
    iPages      = int( dPagination[ "totalPages" ] )
    #
    if iPages > 1:
        #
        # actually iEntries is a minimum, the actual number of entries is more
        #
        iEntries = 1 + ( iPages - 1 ) * int( dPagination[ "entriesPerPage" ] )
        #
    #
    if not iEntries:
        #
        raise SearchGotZeroResults( "search executed OK but returned no items" )
        #
    #
    iTotalItems = iEntries
    #
    lResults = dResponse[ "searchResult" ]
    #
    iThisItem = 0
    #
    for dItem in lResults:
        #
        iThisItem += 1
        #
        dThisItem = {}
        #
        #
        #
        yield dThisItem, iThisItem, iTotalItems
        
    
    