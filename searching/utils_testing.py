from os                 import rename
from os.path            import realpath, join

from core.utils_testing import getTableFromScreenCaptureGenerator


from .tests             import sItemHitLog # in __init__.py

from File.Del           import DeleteIfExists
from File.Test          import isFileThere
from File.Write         import QuietDump

from Time.Convert       import getDateTimeObjFromString   as getDate
from Time.Delta         import getIsoDateTimeNowPlus
from Time.Output        import getIsoDateTimeFromDateTime as getIsoDT


def getItemHitsLog( uHitLogFileContent ):
    #
    oHitsLogIter = getTableFromScreenCaptureGenerator( uHitLogFileContent )
    #
    lHeader = next( oHitsLogIter )
    #
    dNamePosition = {}
    #
    i = 0
    #
    for sName in lHeader:
        #
        dNamePosition[ sName ] = i
        #
        i += 1
        #
    #
    d = dNamePosition
    #
    lItemHits = []
    #
    for lParts in oHitsLogIter:
        #
        dRow = dict( 
                iItemNumb   = lParts[ d['iItemNumb'] ],
                tTimeEnd    = lParts[ d['tTimeEnd' ] ],
                iHitStars   = lParts[ d['iHitStars'] ] )
        #
        lItemHits.append( dRow )
        #
    #
    return lItemHits




def updateHitLogFile( oUserItems, sPathHere ):
    #
    sHitLogFile = join( sPathHere, 'ItemHitsLog.log' )
    sHitLogBack = join( sPathHere, 'ItemHitsLog.bak' )
    #            
    if not isFileThere( sHitLogFile ):
        #
        QuietDump( sItemHitLog, sHitLogFile )
        #
    #
    oHitLogFile = open( sHitLogFile )
    #
    lItemHits = getItemHitsLog( oHitLogFile )
    #
    iBegRows = len( lItemHits )
    #
    # discard rows that are too old
    #
    sDateTimeAgo = getIsoDateTimeNowPlus( -120 )
    #
    lItemHits = [ d for d in lItemHits if d['tTimeEnd' ] > sDateTimeAgo ]
    #
    iEndRows = len( lItemHits )
    #
    setItemNumbsAlready = set( ( int( d['iItemNumb'] ) for d in lItemHits ) )
    #
    iNew = 0
    #
    for oItemHit in oUserItems:
        #
        if oItemHit.iItemNumb_id in setItemNumbsAlready: continue
        #
        dRow = dict(
            iItemNumb   = str(      oItemHit.iItemNumb_id ),
            tTimeEnd    = getIsoDT( oItemHit.iItemNumb.tTimeEnd ),
            iHitStars   = str(      oItemHit.iHitStars ) )
        #
        lItemHits.append( dRow )
        #
        setItemNumbsAlready.add( oItemHit.iItemNumb_id )
        #
        iNew += 1
        #
        if iNew >= 5: break
        #
    #
    if iNew > 0:
        #
        dItemHits = { dItemHits[ d['tTimeEnd'] ] : d for d in lItemHits }
        #
        lKeys = list( dItemHits.keys() )
        #
        lKeys.sort()
        #
        iterItemHits = ( dItemHits[ k ] for k in lKeys )
        #
        lOut = [ ' | '.join( ( d['tTimeEnd'],d['iItemNumb'],d['iHitStars'] ) )
                    for d in iterItemHits ]
        #
        iEndRows = len( lOut )
        #
        lOut[0:0] = [ 'tTimeEnd            | iItemNumb    | iHitStars' ]
        #
        sOut = '\n'.join( lOut )
        #
        DeleteIfExists( sHitLogBack )
        #
        rename( sHitLogFile, sHitLogBack )
        #
        QuietDump( sOut, sHitLogFile )
        #
    #
    return iBegRows, iEndRows

