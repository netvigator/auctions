from json           import load

# from six import print_ as print3

from Dict.Get       import getAnyValue
from Dict.Maintain  import getDictValuesFromSingleElementLists

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass

    
def getSearchResultGenerator( sFile ):
    #
    dResults = load( open( sFile ) )
    #
    # findItemsAdvancedResponse
    # findItemsByCategoryResponse
    # findItemsByKeywordsResponse
    #
    lResponse = getAnyValue( dResults ) # should be only 1 value to get
    #
    if lResponse is None or len( lResponse ) != 1:
        #
        raise SearchNotWorkingError( 'content of "%s" invalid' % sFile )
        #
    #
    dResponse = lResponse[0]
    #
    if dResponse.get( "ack" ) != ["Success"]:
        #
        sMessage = 'ack returned "%s"' % dResponse[ "ack" ][0]
        #
        raise SearchNotWorkingError( sMessage )
        #
    #
    dPagination = dResponse[ "paginationOutput" ][0]
    #
    iEntries    = int( dPagination[ "totalEntries" ][0] )
    #
    iPages      = int( dPagination[ "totalPages" ][0] )
    #
    if iPages > 1:
        #
        # actually iEntries is a minimum, the actual number of entries is more
        #
        iEntries = (
            1 + ( iPages - 1 ) * int( dPagination[ "entriesPerPage" ][0] ) )
        #
    #
    if not iEntries:
        #
        raise SearchGotZeroResults( "search executed OK but returned no items" )
        #
    #
    dPagination[ "totalEntries" ] = dPagination[ "totalEntries" ][0]
    #
    dResultDict = dResponse[ "searchResult" ][0]
    #
    # print3( 'dResultDict.keys():', list( dResultDict.keys() ) )
    #
    iThisItem = 0
    #
    lResults = dResultDict.get('item')
    #
    # print3( 'lResults:', lResults )
    #
    for dItem in lResults:
        #
        iThisItem += 1
        #
        getDictValuesFromSingleElementLists( dItem )
        #
        #
        dPagination["thisEntry"] = str( iThisItem )
        #
        dItem["paginationOutput"]= dPagination
        #
        yield dItem
        
    
    