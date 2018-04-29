from os.path                import join

from core.ebay_api_calls    import getSingleItem

from searching.models       import ItemFound
from searching.utils_test   import getItemHitsLog

def getSingleItemResponseExample():
    
    sHitLogFile = join( 'searching', 'tests', 'ItemHitsLog.log' )

    lItemHits = getItemHitsLog( sHitLogFile )

    setItemNumbs = frozenset( ( int( d['iItemNumb'] ) for d in lItemHits ) )

    lGotItems = ItemFound.objects.filter( pk__in = setItemNumbs ).order_by( '-tTimeEnd' )

    for oItem in lGotItems:
        #
        if True or oItem.bBuyItNowable:
            #
            print( oItem.iItemNumb )
            #
            break
        #
    #
    s = getSingleItem( oItem.iItemNumb )
    #
    return s
