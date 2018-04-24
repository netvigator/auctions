from os                 import rename
from os.path            import realpath, join

from core.utils_test    import ( getTableFromScreenCaptureGenerator,
                                 getNamePositionDict, BaseUserTestCase )

from .models            import Search
from .tests             import sItemHitLog # in __init__.py
from .utilsearch        import getPriorityChoices

from File.Del           import DeleteIfExists
from File.Test          import isFileThere
from File.Write         import QuietDump

from Time.Convert       import getDateTimeObjFromString   as getDate
from Time.Delta         import getIsoDateTimeNowPlus
from Time.Output        import getIsoDateTimeFromDateTime as getIsoDT


class BaseUserTestCaseCanAddSearches( BaseUserTestCase ):
    ''' test getPriorityChoices() '''
    #
    def setUp( self ):
        #
        super( BaseUserTestCaseCanAddSearches, self ).setUp()
        #
        self.client.login(username='username1', password='mypassword')
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
        lOut = [ ' | '.join( ( d['tTimeEnd'],d['iItemNumb'],d['iHitStars'] ) )
                    for d in lItemHits ]
        #
        iEndRows = len( lOut )
        #
        lOut.sort()
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

