from os.path                import join

from core.ebay_api_calls    import getSingleItem

from searching.models       import ItemFound
from searching.utils_test   import getItemHitsLog

from Numb.Get               import getRandomDigits
from Time.Delta             import getIsoDateTimeNowPlus, getDeltaDaysFromISOs

class NoExampleRecords( Exception ): pass



def getSingleItemResponseCandidate( bWantEnded = True ):
    #
    sStillAvailableDate = getIsoDateTimeNowPlus( -89 )
    #
    sHitLogFile = join( 'searching', 'tests', 'ItemHitsLog.log' )
    #
    def getActiveOrEnded( sDate ):
        #
        if bWantEnded:
            #
            bWantThis = int( getDeltaDaysFromISOs( sDate ) ) > 1
            #
        else:
            #
            bWantThis = int( getDeltaDaysFromISOs( sDate ) ) < -1
            #
        #
        return bWantThis
    #
    lItemHits = [ d for d in getItemHitsLog( sHitLogFile )
                  if ( d[ 'tTimeEnd' ] > sStillAvailableDate and
                      getActiveOrEnded( d[ 'tTimeEnd' ] ) ) ]
    #
    lPrioritySelect = []
    #
    for i in range( len( lItemHits ) ):
        #
        d = lItemHits[ i ]
        #
        iDaysAgo = int( getDeltaDaysFromISOs( d[ 'tTimeEnd' ] ) )
        #
        lPrioritySelect.append( ( iDaysAgo * 3 + int( d[ 'iHitStars' ] ), i ) )
        #
    #
    if not lPrioritySelect:
        #
        sayWhich = 'ended' if bWantEnded else 'active'
        #
        raise NoExampleRecords( 'no %s records in %s!' %
                               ( sayWhich, sHitLogFile ) )
        #
    #
    lPrioritySelect.sort()
    lPrioritySelect.reverse()
    #
    iTryThis = len( lPrioritySelect ) + 1
    #
    while iTryThis > len( lPrioritySelect ):
        #
        iTryThis = int( getRandomDigits(1) )
        #
    #
    dTryThis = lItemHits[ lPrioritySelect[ iTryThis ][1] ]
    #
    # s = getSingleItem( dTryThis[ 'iItemNumb' ] )
    #
    return dTryThis
