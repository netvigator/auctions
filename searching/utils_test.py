from os                 import rename
from os.path            import realpath, join

from core.utils_test    import ( getTableFromScreenCaptureGenerator,
                                 getNamePositionDict, BaseUserWebTestCase )

from .models            import Search
from .tests             import sItemHitLog # in __init__.py
from .utilsearch        import getPriorityChoices

from pyPks.File.Del     import DeleteIfExists
from pyPks.File.Test    import isFileThere
from pyPks.File.Write   import QuietDump

from pyPks.Time.Convert import getDateTimeObjFromString   as getDate
from pyPks.Time.Delta   import getIsoDateTimeNowPlus
from pyPks.Time.Output  import getIsoDateTimeFromDateTime as getIsoDT


class BaseUserWebTestCaseCanAddSearches( BaseUserWebTestCase ):
    ''' test getPriorityChoices() '''
    #
    def setUp( self ):
        #
        super( BaseUserWebTestCaseCanAddSearches, self ).setUp()
        #
        self.addSearch( "My clever search c", 'C1', self.user1 )
        #
        self.addSearch( "My clever search D", 'D2', self.user1 )
        #
        self.addSearch( "My clever search 2", 'A1', self.user1 )
        #
    #
    def addSearch( self, cTitle, cPriority, oUser ):
        oSearch     = Search(
                        cTitle      = cTitle,
                        cPriority   = cPriority,
                        iUser       = oUser )
        #
        oSearch.save()

    #
    def getPriorityChoices( self, oUser, sThisPriority = None ):
        #
        return getPriorityChoices( Search, oUser, sThisPriority )


def getItemHitsLog( sPathFile ):
    #
    oHitsLogIter = getTableFromScreenCaptureGenerator( open( sPathFile ) )
    #
    lHeader = next( oHitsLogIter )
    #
    d = getNamePositionDict( lHeader )
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
    lItemHits = getItemHitsLog( sHitLogFile )
    #
    iBegRows = len( lItemHits )
    #
    # discard rows that are too old
    #
    sDateTimeAgo = getIsoDateTimeNowPlus( -100 )
    #
    lItemHits = [ d for d in lItemHits if d['tTimeEnd' ] > sDateTimeAgo ]
    #
    iEndRows = len( lItemHits )
    #
    setItemNumbsAlready = set( ( int( d['iItemNumb'] ) for d in lItemHits ) )
    #
    iNew = 0
    #
    tTargetStars = ( 400, 350, 300, 250, 200 )
    #
    for iTargetStars in tTargetStars:
        #
        for oItemHit in oUserItems:
            #
            if oItemHit.iItemNumb_id in setItemNumbsAlready: continue
            #
            if oItemHit.iHitStars < iTargetStars: continue
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
        lOut = [ ' | '.join( ( d['tTimeEnd'],d['iItemNumb'],d['iHitStars'] ) )
                    for d in lItemHits ]
        #
        iEndRows = len( lOut )
        #
        lOut.sort()
        #
        lOut[0:0] = [ 'tTimeEnd            | iItemNumb    | iHitStars' ]
        #
        sOut = '%s\n' % '\n'.join( lOut )
        #
        DeleteIfExists( sHitLogBack )
        #
        rename( sHitLogFile, sHitLogBack )
        #
        QuietDump( sOut, sHitLogFile )
        #
    #
    return iBegRows, iEndRows

