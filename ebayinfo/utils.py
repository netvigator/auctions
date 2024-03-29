from logging            import getLogger
from os.path            import join
from time               import sleep

from psycopg2           import OperationalError

from django.conf        import settings
from django.db          import DataError, connection
from django.db.utils    import IntegrityError

from core.dj_import     import ET # xml.etree.ElementTree
from core.dj_import     import ObjectDoesNotExist

from core.utils         import ( getNamerSpacer,
                                 getBegTime, sayDuration )

# in __init__.py
from ebayinfo           import dMarketsRelated, EBAY_FILES_FOLDER

from .models            import EbayCategory, Market, CategoryHierarchy

from pyPks.Dict.Get         import getReverseDictGotUniqueItems
from pyPks.File.Del         import DeleteIfExists
from pyPks.File.Write       import QuietDump
from pyPks.String.Output    import ReadableNo
from pyPks.Utils.Progress   import TextMeter, DummyMeter
from pyPks.Web.HTML         import getChars4HtmlCodes

logger = getLogger(__name__)

class UnexpectedResponse( Exception ): pass

'''
utils for handling info from ebay API
note the actual calls to the ebay API are in
core.ebay_wrapper.py
'''

# variable referenced in tests
CATEGORY_VERSION_FILE = join( EBAY_FILES_FOLDER, 'Categories_Ver_%s.xml' )
CATEGORY_LISTING_FILE = join( EBAY_FILES_FOLDER, 'Categories_All_%s.xml' )

sRootTag = 'GetCategoriesResponse'

sNamerSpacer, sRootNameSpTag = getNamerSpacer( sRootTag,
                sXmlNameSpace = 'urn:ebay:apis:eBLBaseComponents' )


tVersionChildTags = (
    'Timestamp', 'Ack', 'Version', 'Build', 'UpdateTime', 'CategoryVersion' )

tListingChildTags = (
    'Timestamp', 'Ack', 'Version', 'Build', 'UpdateTime', 'CategoryVersion',
    'CategoryCount', )

tCategoryArrayTags = (
    'CategoryID', 'CategoryLevel', 'CategoryName', 'CategoryParentID',
    'LeafCategory' )


def _getTagsValuesGotRoot( root, tTags = tVersionChildTags, sFile = None ):
    #
    if root.tag != sRootNameSpTag:
        #
        raise UnexpectedResponse(
            'Check file %s for correct output!' % sFile  )
        #
    #
    dTagsValues = {}
    #
    for sChildTag in tTags:
        #
        try:
            dTagsValues[ sChildTag ] = root.find(
                                        sNamerSpacer % sChildTag ).text
        except AttributeError:
            raise( UnexpectedResponse(
                'Check file %s for tag "%s"!' %
                ( sFile , sChildTag ) ) )
            #
    #
    if dTagsValues[ 'Ack' ] != 'Success':
        raise( UnexpectedResponse(
            'Check file %s for tag "Ack" -- should be "Success"!' % sFile ) )
    #
    return dTagsValues


def _getCategoryIterable(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117' ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    dTagsValues = _getTagsValuesGotRoot(
            root, tTags = tListingChildTags, sFile = sFile )
    #
    if dTagsValues[ 'CategoryVersion' ] != sWantVersion:
        #
        raise( UnexpectedResponse(
            'Check file %s for tag "CategoryVersion" -- should be %s!' %
            ( sFile , sWantVersion ) ) )
        #
    #
    oCategories = root.find( sNamerSpacer % 'CategoryArray' )
    #
    return oCategories.findall( sNamerSpacer % 'Category' ), dTagsValues



def _countCategories(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117',
        bSayCount = False ):
    #
    oCategories, dTagsValues = _getCategoryIterable( sFile, sWantVersion )
    #
    i = 0
    #
    for oCategory in oCategories:
        #
        i += 1
        #
    #
    if bSayCount:
        print( 'CategoryCount line said',
            ReadableNo( dTagsValues[ 'CategoryCount' ] ),
                'categories, actully counted', ReadableNo( i ) )
    #
    return dTagsValues[ 'CategoryCount' ], i



def _getCategoryDictGenerator(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117' ):
    #
    oCategories, dTagsValues = _getCategoryIterable( sFile, sWantVersion )
    #
    for oCategory in oCategories:
        #
        dCategory = {}
        #
        for sAttribute in tCategoryArrayTags:
            #
            oGotAttribute = oCategory.find( sNamerSpacer % sAttribute )
            #
            if oGotAttribute is None:
                sSayAttribute = ''
            else:
                sSayAttribute = oGotAttribute.text
            #
            dCategory[ sAttribute ] = sSayAttribute
            #
        #
        dCategory [ 'CategoryVersion' ] = dTagsValues[ 'CategoryVersion' ]
        #
        yield dCategory


'''
categoryDictIterable = _getCategoryDictGenerator()
pprint( next( categoryDictIterable ) )
returns
{'CategoryID': '20081',
 'CategoryLevel': '1',
 'CategoryName': 'Antiques',
 'CategoryParentID': '20081',
 'CategoryVersion': EBAY_US_CURRENT_VERSION,
 'LeafCategory': ''}
'''

def _getCategoryListParams( uMarket, uWantVersion ):
    #
    '''pass market name (such as EBAY-US) and version you want
    returns tuple (market query object, market name, string version)'''
    #
    if isinstance( uMarket, int ):
        oMarket = Market.objects.get( iEbaySiteID = uMarket )
        sMarket = oMarket.cMarket
        # uMarket = sMarket
    elif isinstance( uMarket, str ):
        oMarket = Market.objects.get( cMarket = uMarket )
        sMarket = uMarket
    else:
        oMarket = uMarket
        sMarket = oMarket.cMarket
    #
    if isinstance( uWantVersion, str ):
        sWantVersion =      uWantVersion
    else:
        sWantVersion = str( uWantVersion )
    #
    return oMarket, sMarket, sWantVersion





def _putCategoriesInDatabase(
            uMarket         = 'EBAY-US', # expect str but obj OK
            uWantVersion    = '120',     # expect str but int OK
            bShowProgress   = False,
            sFile           = None ):
    #
    t = _getCategoryListParams( uMarket, uWantVersion )
    #
    oMarket, sMarket, sWantVersion = t
    #
    # _getCategoryDictGenerator checks for the expected version
    #
    if sFile is None:
        #
        sFile = CATEGORY_LISTING_FILE % sMarket
        #
    #
    categoryDictIterable = _getCategoryDictGenerator(
        sFile = sFile, sWantVersion = sWantVersion )
    #
    if bShowProgress: # progress meter for running in shell, no need to test
        #
        oProgressMeter = TextMeter( use_hours = True )
        #
        print( 'counting categories ...' )
        #
        iCount = 0
        #
        for dCategory in categoryDictIterable: iCount +=1
        #
        categoryDictIterable = _getCategoryDictGenerator(
            sFile = CATEGORY_LISTING_FILE % sMarket,
            sWantVersion = sWantVersion )
        #
        sLineB4 = 'stepping thru ebay categories ...'
        sOnLeft = "%s %s" % ( ReadableNo( iCount ), 'categories' )
        #
        oProgressMeter.start( iCount, sOnLeft, sLineB4 )
        #
    else:
        #
        oProgressMeter = DummyMeter()
        #
    #
    iWantVersion = int( sWantVersion )
    #
    oRoot = EbayCategory()
    #
    try: # look for a root category for this market & tree version
        #
        oRoot = EbayCategory.objects.get(
            iEbaySiteID     = oMarket,
            iCategoryID     = 0 )
        #
        if oRoot.iTreeVersion != iWantVersion:
            #
            oRoot.name      = (
                '%s version %s Root' % ( sMarket, sWantVersion ) )
            #
            oRoot.iTreeVersion = iWantVersion
            #
            oRoot.save()
            #
        #
    except ObjectDoesNotExist: # if the root is not there yet, put it in
        #
        oRoot = EbayCategory(
            name            = (
                '%s version %s Root' % ( sMarket, sWantVersion ) ),
            iCategoryID     = 0,
            iEbaySiteID     = oMarket,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRoot.save()
        #
    iSeq = 0
    #
    try:
        #
        for dCategory in categoryDictIterable:
            #
            iSeq  += 1
            #
            oProgressMeter.update( iSeq )
            #
            sConfirmVersion = dCategory['CategoryVersion']
            #
            oCategory = EbayCategory()
            #
            try:
                #
                oCategory = EbayCategory.objects.get(
                    iEbaySiteID     = oMarket,
                    iCategoryID     = int( dCategory['CategoryID'] ) )
                #
            except ObjectDoesNotExist:
                #
                oCategory = EbayCategory(
                    iCategoryID     = int( dCategory['CategoryID'] ),
                    iEbaySiteID     = oMarket )
            #
            sCategoryName = getChars4HtmlCodes( dCategory['CategoryName'] )
            #
            oCategory.name          = sCategoryName
            oCategory.iLevel        = int( dCategory['CategoryLevel'   ] )
            oCategory.bLeafCategory = bool(dCategory['LeafCategory'    ] )
            oCategory.iTreeVersion  = iWantVersion
            oCategory.iParentID     = int( dCategory['CategoryParentID'] )
            #
            if dCategory['CategoryID'] == dCategory['CategoryParentID']:
                #
                # level 1 category, CategoryID == CategoryParentID
                #
                oCategory.parent = oRoot
                #
            else:
                #
                oCategory.parent = EbayCategory.objects.get(
                    iEbaySiteID = oMarket,
                    iCategoryID = dCategory['CategoryParentID'],
                    iTreeVersion= iWantVersion )
                #
            #
            try:
                oCategory.save()
            except DataError:
                raise DataError( 'too long: %s' % sCategoryName )
            #
        #
        oProgressMeter.end( iSeq )
        #
        oMarket.iCategoryVer = int( sWantVersion )
        #
        oMarket.save()
        #
        # list is updated, must redo store hierarchies
        #
        # CategoryHierarchy.objects.filter( iEbaySiteID = oMarket ).delete()
        #
        # cannot delete!!!  rows may be referenced by itemsfound!!!
        #
        #
    except OperationalError: # downloaded file not complete!
        #
        sMessage = 'ebay categories file %s is incomplete!' % sFile
        #
        logger.error( sMessage )
        #





def getCategoryListThenStore(
            uMarket         = 'EBAY-US', # expect str but int or obj OK
            uWantVersion    = '119',     # expect str but int OK
            bUseSandbox     = False,
            bShowProgress   = False ):
    #
    '''When ebay updates its category list for a market,
    the bot can download a text table of the current categories
    from the ebay api.
    This high level function
    fetches the list from ebay
    then updates the database with the new info.
    Note that ebay usually puts out updates categories
    for several markets all together (suddenly).
    '''
    # circular import problem, this must be here not at top
    from core.ebay_api_calls import getMarketCategoriesGotGlobalID
    #
    t = _getCategoryListParams( uMarket, uWantVersion )
    #
    oMarket, sMarket, sWantVersion = t
    #
    if bShowProgress:
        print('')
        print( 'fetching category list for %s ....' % sMarket )
    #
    sCategories = getMarketCategoriesGotGlobalID(
            sGlobalID = sMarket, bUseSandbox = bUseSandbox )
    #
    QuietDump( sCategories, CATEGORY_LISTING_FILE % sMarket )
    #
    _putCategoriesInDatabase(
            uMarket         = sMarket,
            uWantVersion    = sWantVersion,
            bShowProgress   = bShowProgress )



def _getCategoryVersionValues( sFile ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    return _getTagsValuesGotRoot( root, sFile = sFile )



def _getCategoryVersionFromFile(
            sGlobalID = 'EBAY-US', sFile = CATEGORY_VERSION_FILE ):
    #
    '''get the version from a file already downloaded
    values from a downloaded file are all strings, right?!
    this returns an integer (if it works)'''
    #
    dTagsValues = _getCategoryVersionValues( sFile % sGlobalID )
    #
    return int( dTagsValues[ 'CategoryVersion' ] )





def _getDictMarket2SiteID():
    #
    dMarket2SiteID   = {}
    dSiteID2ListVers = {}
    #
    for oMarket in Market.objects.all():
        #
        dMarket2SiteID[   oMarket.cMarket     ] = oMarket.iEbaySiteID
        dSiteID2ListVers[ oMarket.iEbaySiteID ] = oMarket.iCategoryVer
        #
    #
    dSiteID2Market = getReverseDictGotUniqueItems( dMarket2SiteID )
    #
    return dMarket2SiteID, dSiteID2Market, dSiteID2ListVers


dMarket2SiteID, dSiteID2Market, dSiteID2ListVers = _getDictMarket2SiteID()

'''
pprint( dMarket2SiteID )
{'EBAY-AT':      16,
 'EBAY-AU':      15,
 'EBAY-CH':     193,
 'EBAY-DE':      77,
 'EBAY-ENCA':     2,
 'EBAY-ES':     186,
 'EBAY-FR':      71,
 'EBAY-FRBE':    23,
 'EBAY-FRCA':   210,
 'EBAY-GB':       3,
 'EBAY-HK':     201,
 'EBAY-IE':     205,
 'EBAY-IN':     203,
 'EBAY-IT':     101,
 'EBAY-MOTOR':  100,
 'EBAY-MY':     207,
 'EBAY-NL':     146,
 'EBAY-NLBE':   123,
 'EBAY-PH':     211,
 'EBAY-PL':     212,
 'EBAY-SE':     218,
 'EBAY-SG':     216,
 'EBAY-US':       0 }
 '''


def _getCheckCategoryVersion(
            iSiteId     = 0,
            sGlobalID   = None,
            sFile       = CATEGORY_VERSION_FILE,
            bUseSandbox = False ):
    #
    '''call the ebay API to get the info, extract the version from that'''
    #
    # circular import problem, this must be here not at top
    from core.ebay_api_calls    import ( getCategoryVersionGotGlobalID,
                                         getCategoryVersionGotSiteID )
    # iSiteId = 0 aka sGlobalID = 'EBAY-US'
    #
    if sGlobalID  is None:
        #
        sResponse = getCategoryVersionGotSiteID(
                        iSiteId, bUseSandbox = bUseSandbox )
        #
        sGlobalID = dSiteID2Market[ int( iSiteId ) ]
        #
    else:
        #
        sResponse = getCategoryVersionGotGlobalID(
                        sGlobalID, bUseSandbox = bUseSandbox )
        #
    #
    QuietDump( sResponse, sFile % sGlobalID )
    #
    iVersion = _getCategoryVersionFromFile( sGlobalID, sFile )
    #
    DeleteIfExists( EBAY_FILES_FOLDER, sFile % sGlobalID )
    #
    return iVersion



def getWhetherAnyEbayCategoryListsAreUpdated( bUseSandbox = False ):
    #
    '''For each market, this queries ebay,
    compares ebay's latest category version with the database.
    returns: tuple of markets
    markets with a newer category list version are in the tuple
    '''
    #
    lMarketsHaveNewerCategoryVersionLists = []
    #
    iTotalSites = len( dSiteID2ListVers )
    #
    i = 0
    #
    for iSiteID in dSiteID2ListVers:
        #
        i += 1
        #
        iEbayHas = _getCheckCategoryVersion(
            iSiteId     = iSiteID,
            bUseSandbox = bUseSandbox )
        #
        # when testing, must access the database directly to work right!
        #
        iTableHas = dSiteID2ListVers[ iSiteID ]
        #
        if iEbayHas != iTableHas:
            #
            d = dict( iSiteID   = iSiteID,
                      iEbayHas  = iEbayHas,
                      iTableHas = iTableHas )
            #
            lMarketsHaveNewerCategoryVersionLists.append( d )
            #
        #
        if i < iTotalSites: sleep(1)
        #
    #
    return lMarketsHaveNewerCategoryVersionLists



def getShowMarketsHaveNewerCategoryVersionLists():
    #
    lNewerCategories = getWhetherAnyEbayCategoryListsAreUpdated()
    #
    lMarketsHaveNewerCategoryVersionLists = []
    #
    if lNewerCategories:
        #
        lNew = [ ( d['iSiteID'], d ) for d in lNewerCategories ]
        #
        lNew.sort()
        #
        lMarkets = [ t[1] for t in lNew ]
        #
        lMarketsHaveNewerCategoryVersionLists = [
            '    %3s |       %3s |      %3s' %
            ( d['iSiteID'], d['iTableHas'], d['iEbayHas'] )
            for d in lMarkets ]
        #
        lMarketsHaveNewerCategoryVersionLists[0:0] = [
            'Site ID | Table Has | Ebay Has' ]
        #
    #
    return lMarketsHaveNewerCategoryVersionLists


def _getCategoryHierarchyID(
            iCategoryID, sCategoryName, iEbaySiteID, dEbayCatHierarchies ):
    #
    tCategoryID = iCategoryID, iEbaySiteID
    #
    iCatHeirarchy = None
    #
    tRelatedMarkets = dMarketsRelated.get( iEbaySiteID, () )
    #
    while True: # 2 or 3 loops possible if ebay-us or ebay-motor
        #
        if tCategoryID in dEbayCatHierarchies:
            #
            iCatHeirarchy = dEbayCatHierarchies[ tCategoryID ]
            #
            # bOkCatHeirarchy =
            # CategoryHierarchy.objects.filter( pk = iCatHeirarchy ).exists()
            #
        elif CategoryHierarchy.objects.filter(
                                iCategoryID = iCategoryID,
                                iEbaySiteID = iEbaySiteID ).exists():
            #
            iCatHeirarchy = CategoryHierarchy.objects.get(
                                iCategoryID = iCategoryID,
                                iEbaySiteID = iEbaySiteID ).pk
            #
            dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
            #
        elif EbayCategory.objects.filter(
                                iCategoryID = iCategoryID,
                                iEbaySiteID = iEbaySiteID ).exists():
            #
            oEbayCategory   = EbayCategory.objects.get(
                                iCategoryID = iCategoryID,
                                iEbaySiteID = iEbaySiteID )
            #
            lCatHeirarchy = [ oEbayCategory.name ]
            #
            while oEbayCategory.iLevel > 1:
                #
                oParentCat = oEbayCategory.parent
                #
                if oParentCat:
                    lCatHeirarchy.append( oParentCat.name )
                else:
                    #
                    break
                    #
                #
                oEbayCategory = oParentCat
                #
            #
            lCatHeirarchy.reverse()
            #
            # sCatHeirarchy = '\r'.join( lCatHeirarchy ) # django uses return, but
            # return only does not work in shell, each line overwrites the prior one
            sCatHeirarchy = ', '.join( lCatHeirarchy ) # should show better
            #
            oMarket = Market.objects.get( iEbaySiteID = iEbaySiteID )
            #
            oCategoryHierarchy = CategoryHierarchy(
                    iCategoryID     = iCategoryID,
                    iEbaySiteID     = oMarket,
                    cCatHierarchy   = sCatHeirarchy )
            #
            oCategoryHierarchy.save()
            #
            iCatHeirarchy = oCategoryHierarchy.pk
            #
            dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
            #
        elif (  tRelatedMarkets and
                EbayCategory.objects.filter(
                        iCategoryID = iCategoryID,
                        iEbaySiteID = tRelatedMarkets[0] )
                        .exists() ): # EBAY-US : EBAY-MOTOR & vice versa
                #
                iEbaySiteID = tRelatedMarkets[0]
                tCategoryID = iCategoryID, iEbaySiteID
                #
                continue
                #
        elif (  len( tRelatedMarkets ) > 1 and
                EbayCategory.objects.filter(
                        iCategoryID = iCategoryID,
                        iEbaySiteID = tRelatedMarkets[-1] )
                        .exists() ): # EBAY-US : EBAY-MOTOR & vice versa
                #
                iEbaySiteID = tRelatedMarkets[-1]
                tCategoryID = iCategoryID, iEbaySiteID
                #
                continue
                #
            #
        #
        break
        #
    #
    if iCatHeirarchy is None: # testing glitch, limited set of categories
        #
        iCatHeirarchy = sCategoryName
        #
        if settings.TESTING:
            #
            # test database does not have all categories
            #
            pass
            #
        else:
            #
            sMessage = ( 'For market %s,  '
                        '%s does not exist' %
                            ( iEbaySiteID, iCategoryID ) )
            #
            logger.info( sMessage )
            #
        #
    #
    return iCatHeirarchy



def getEbayCategoryHierarchies( dItem, dEbayCatHierarchies ):
    #
    ''' return the ebay category hierarchy(ies) for a search find item
    that is, this returns the id(s) of the category hierarchy table row(s)
    note:
    1) items can optionally have a secondary category
    2) this function has a side effect, it updates dEbayCatHierarchies
    '''
    #
    iCategoryID = int( dItem.get( 'primaryCategory' ).get( 'categoryId' ) )
    sCategoryName =    dItem.get( 'primaryCategory' ).get( 'categoryName' )
    #
    iEbaySiteID = dMarket2SiteID.get( dItem.get( 'globalId' ) )
    #
    iCatHeirarchy = _getCategoryHierarchyID(
                        iCategoryID, sCategoryName, iEbaySiteID, dEbayCatHierarchies )
    #
    s2ndCategoryID = dItem.get( 'secondaryCategory', {} ).get( 'categoryId' )
    #
    if s2ndCategoryID:
        #
        i2ndCategoryID = int( s2ndCategoryID )
        #
        sCategoryName = dItem.get( 'secondaryCategory' ).get( 'categoryName' )
        #
        i2ndCatHeirarchy = _getCategoryHierarchyID(
                    i2ndCategoryID,
                    sCategoryName,
                    iEbaySiteID,
                    dEbayCatHierarchies )
        #
    else:
        #
        i2ndCatHeirarchy = None
        #
    #
    return iCatHeirarchy, i2ndCatHeirarchy




def getCategoryListsUpdated( bConsoleOut = False ):
    #
    if bConsoleOut:
        #
        oBeg = getBegTime( bConsoleOut )
        #
    #
    lNeedUpdates = getWhetherAnyEbayCategoryListsAreUpdated()
    #
    if lNeedUpdates:
        #
        print('')
        print('Need updates for:')
        #
        for d in lNeedUpdates:
            #
            print('  %s' % dSiteID2Market[ d['iSiteID'] ] )
            #
        #
        print('')
        #
    #
    for d in lNeedUpdates:
        #
        getCategoryListThenStore(
                uMarket         = d['iSiteID'],
                uWantVersion    = d['iEbayHas'],
                bShowProgress   = bConsoleOut )
        #
    #
    if bConsoleOut:
        #
        sayDuration( oBeg )



def updateCategoryHierarchies(): # run after ebay category update
    #
    sCommand = (
     """select p."iCategoryID", p."iEbaySiteID_id", c.name
        from category_hierarchies p
        left outer join ebay_categories c
            on  c."iCategoryID" = p."iCategoryID" and
                c."iEbaySiteID_id" = p."iEbaySiteID_id"
            where p."cCatHierarchy" not like '%' || c.name ;""" )
    #
    # select right( 'Business & Industrial, Electrical & Test Equipment, Test, Measurement & Inspection, Test Meters & Detectors, LCR & Impedance Meters', position( ' ,' in  reverse( 'Business & Industrial, Electrical & Test Equipment, Test, Measurement & Inspection, Test Meters & Detectors, LCR & Impedance Meters' ) ) ) ;
    #
    cursor = connection.cursor()
    cursor.execute( sCommand )
    #
    lNeedUpdates = cursor.fetchall()
    #
    dEbayCatHierarchies = {}
    #
    for t in lNeedUpdates:
        #
        iCategoryID, iEbaySiteID, sCategoryName = t
        #
        try:
            #
            CategoryHierarchy.objects.filter(
                                    iCategoryID = iCategoryID,
                                    iEbaySiteID = iEbaySiteID ).delete()
            #
        except IntegrityError:
            #
            pass # maybe next time
            #
        #
        if iEbaySiteID in dMarketsRelated: # EBAY-US : EBAY-MOTOR & vice versa
            #
            try:
                #
                CategoryHierarchy.objects.filter(
                    iCategoryID = iCategoryID,
                    iEbaySiteID = dMarketsRelated.get( iEbaySiteID ) ).delete()
                #
            except IntegrityError:
                #
                pass # maybe next time
                #
            #
        #
        _getCategoryHierarchyID(
                iCategoryID, sCategoryName, iEbaySiteID, dEbayCatHierarchies )
        #



def setShippingTypeLocalPickupOptional( dNewResult ):
    #
    '''
    if shippingType is 5 FreePickup, it means
      "Free Local Pick Up" is optional if handlingTime is set, but
      "Local Pick Up ONLY" if handlingTime is not set
    this needs to be set after reading the api data and before the form
    tested in searching/tests/test_models.py (odd location) BECAUSE
    cannot test in tests/test_utils.py BECAUSE
    circular import problem, neither works --
    searching/tests/test_utils.py imports LiveTestGotCurrentEbayCategories
    (the convenient result is test for status of sample live items)
    '''
    #
    iShippingType = dNewResult.get( 'iShippingType' )
    iHandlingTime = dNewResult.get( 'iHandlingTime' )
    #
    if iShippingType == 5 and iHandlingTime and iHandlingTime > 0:
        #
        dNewResult[ 'iShippingType' ] = 9
        #
    #

# def getCategoryForRelatedMarket( iEbaySiteID, iCategoryID ):
# move code from searching/utils.py
# look for
# tRelatedSites = dMarketsRelated.get( iEbaySiteID, () )

'''
select "iCategoryID","cCategory","iCatHeirarchy_id","i2ndCategoryID","c2ndCategory","i2ndCatHeirarchy_id","iEbaySiteID_id" from itemsfound limit 2 ;
 iCategoryID |      cCategory      | iCatHeirarchy_id | i2ndCategoryID | c2ndCategory | i2ndCatHeirarchy_id | iEbaySiteID_id
-------------+---------------------+------------------+----------------+--------------+---------------------+----------------
       38034 | 1930-49             |                  |              0 |              |                     |              0
       73374 | Vintage Televisions |                  |              0 |              |                     |              0

def _fillInCategoryHierarchiesObliteratedByMistake():
    #
    from finders.models import ItemFound
    #
    dEbayCatHierarchies = {}
    #
    oProgressMeter = TextMeter()
    #
    print('')
    print('counting items found ...' )
    #
    oItemsFound = ItemFound.objects.all()
    #
    iCount = len( oItemsFound )
    #
    sLineB4 = 'stepping thru items found ...'
    sOnLeft = "%s %s" % ( ReadableNo( iCount ), 'items found' )
    #
    oProgressMeter.start( iCount, sOnLeft, sLineB4 )
    #
    iSeq = 0
    #
    for oItem in oItemsFound:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        #
        iCatHeirarchy = _getCategoryHierarchyID(
                oItem.iCategoryID,
                oItem.cCategory,
                oItem.iEbaySiteID_id,
                dEbayCatHierarchies )
        #
        bSave = False
        #
        if isinstance( iCatHeirarchy, int ):
            #
            oItem.iCatHeirarchy_id = iCatHeirarchy
            #
            bSave = True
            #
        else:
            #
            print('cannot get CatHeirarchy for iItemNumb: %s ' %
                   oItem.iItemNumb )
            #
        #
        if oItem.i2ndCategoryID:
            #
            i2ndCatHeirarchy = _getCategoryHierarchyID(
                        oItem.i2ndCategoryID,
                        oItem.c2ndCategory,
                        oItem.iEbaySiteID_id,
                        dEbayCatHierarchies )
            #
            if isinstance( i2ndCatHeirarchy, int ):
                #
                oItem.i2ndCatHeirarchy_id = i2ndCatHeirarchy
                #
                bSave = True
                #
            else:
                #
                print('cannot get CatHeirarchy for iItemNumb: %s ' %
                    oItem.iItemNumb )
                #
            #
        #
        if bSave:
            #
            oItem.save()
            #
        #

    #
    oProgressMeter.end( iSeq )
    #



when ebay categories have been updated,
to update application categories:
from ebayinfo.utils import getCategoryListsUpdated
getCategoryListsUpdated( bConsoleOut = True )


CRASH 2019-10-19 after updating EBAY-AU
IntegrityError: update or delete on table "category_hierarchies" violates foreign key constraint "itemsfound_iCatHeirarchy_id_1ebfb2e6_fk_category_hierarchies_id" on table "itemsfound"
DETAIL:  Key (id)=(473) is still referenced from table "itemsfound".

check whether there are unreferenced rows:

select count("iCategoryID") from category_hierarchies where "iCategoryID" not in
    ( select "iCatHeirarchy_id" as icathei from itemsfound
      union
      select "i2ndCatHeirarchy_id" as icathei from itemsfound ) ;

goal: update ebay_categories on a server other than the live one
so instead of bogging down the live server for weeks,
a dedicated server is devoted to this job
then take the live server down for maintenance and update:
1) markets
2) ebay_categories
3) category_hierarchies - this one is not from ebay but composed for this app


get commands from office datbase server:
generic example: pg_dump --data-only --table=tablename sourcedb > onetable.pg

in postgres user on server

pg_dump --data-only --table=markets auctions > /tmp/markets.pg
pg_dump --data-only --table=ebay_categories auctions > /tmp/ebay_categories.pg


markets referenced by:

TABLE "category_hierarchies" CONSTRAINT "category_hierarchies_iEbaySiteID_id_30db3771_fk_markets_i" FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") DEFERRABLE INITIALLY DEFERRED

TABLE "itemsfound" CONSTRAINT "itemsfound_iEbaySiteID_id_306e5c7e_fk_markets_iEbaySiteID" FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") DEFERRABLE INITIALLY DEFERRED


ebay_categories

Foreign-key constraints:
"ebay_categories_parent_id_7e1b74c0_fk_ebay_categories_id" FOREIGN KEY (parent_id) REFERENCES ebay_categories(id) DEFERRABLE INITIALLY DEFERRED

referenced by:

TABLE "itemsfound" CONSTRAINT "itemsfound_i2ndCategoryID_id_e82cd6de_fk_ebay_categories_id" FOREIGN KEY ("i2ndCategoryID_id") REFERENCES ebay_categories(id) DEFERRABLE INITIALLY DEFERRED

TABLE "itemsfound" CONSTRAINT "itemsfound_iCategoryID_id_67c1d3f6_fk_ebay_categories_id" FOREIGN KEY ("iCategoryID_id") REFERENCES ebay_categories(id) DEFERRABLE INITIALLY DEFERRED

TABLE "searching" CONSTRAINT "searching_iEbayCategory_id_9fe370a3_fk_ebay_categories_id" FOREIGN KEY ("iEbayCategory_id") REFERENCES ebay_categories(id) DEFERRABLE INITIALLY DEFERRED

markets referenced by:

TABLE "category_hierarchies" CONSTRAINT "category_hierarchies_iEbaySiteID_id_30db3771_fk_markets_i" FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") DEFERRABLE INITIALLY DEFERRED

TABLE "itemsfound" CONSTRAINT "itemsfound_iEbaySiteID_id_306e5c7e_fk_markets_iEbaySiteID" FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") DEFERRABLE INITIALLY DEFERRED

category_hierarchies

Foreign-key constraints:
"category_hierarchies_iEbaySiteID_id_30db3771_fk_markets_i" FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") DEFERRABLE INITIALLY DEFERRED

Referenced by:
TABLE "itemsfound" CONSTRAINT "itemsfound_i2ndCatHeirarchy_id_2557c784_fk_category_" FOREIGN KEY ("i2ndCatHeirarchy_id") REFERENCES category_hierarchies(id) DEFERRABLE INITIALLY DEFERRED
TABLE "itemsfound" CONSTRAINT "itemsfound_iCatHeirarchy_id_1ebfb2e6_fk_category_hierarchies_id" FOREIGN KEY ("iCatHeirarchy_id") REFERENCES category_hierarchies(id) DEFERRABLE INITIALLY DEFERRED


open psql and auctions database
if on HK office desktop
psql -h data -p 5432 -U <user name> auctions
or if in postgres user on data server
psql -U <user name> auctions
then
ALTER TABLE "category_hierarchies" DROP CONSTRAINT "category_hierarchies_iEbaySiteID_id_30db3771_fk_markets_i" ;
ALTER TABLE "itemsfound" DROP CONSTRAINT "itemsfound_iEbaySiteID_id_306e5c7e_fk_markets_iEbaySiteID" ;
ALTER TABLE "itemsfound" DROP CONSTRAINT "itemsfound_iCategoryID_id_67c1d3f6_fk_ebay_categories_id" ;
ALTER TABLE "itemsfound" DROP CONSTRAINT "itemsfound_i2ndCategoryID_id_e82cd6de_fk_ebay_categories_id" ;
ALTER TABLE "searching" DROP CONSTRAINT "searching_iEbayCategory_id_9fe370a3_fk_ebay_categories_id" ;

truncate table ebay_categories ;
truncate table markets ;

from shell in postgres user:

HK (now main server)
psql -h data -p 5432 -U <user name> auctions < markets.pg
psql -h data -p 5432 -U <user name> auctions < ebay_categories.pg

remotely on data server
psql -U <user name> auctions < /tmp/markets.pg
psql -U <user name> auctions < /tmp/ebay_categories.pg

psql -U <user name> auctions

ALTER TABLE "category_hierarchies" ADD CONSTRAINT "category_hierarchies_iEbaySiteID_id_30db3771_fk_markets_i"
 FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") ON DELETE NO ACTION ;
ALTER TABLE "itemsfound" ADD CONSTRAINT "itemsfound_iEbaySiteID_id_306e5c7e_fk_markets_iEbaySiteID"
 FOREIGN KEY ("iEbaySiteID_id") REFERENCES markets("iEbaySiteID") ON DELETE NO ACTION ;
ALTER TABLE "itemsfound" ADD CONSTRAINT "itemsfound_iCategoryID_id_67c1d3f6_fk_ebay_categories_id"
 FOREIGN KEY ("iCategoryID_id") REFERENCES ebay_categories(id) ON DELETE NO ACTION ;
ALTER TABLE "itemsfound" ADD CONSTRAINT "itemsfound_i2ndCategoryID_id_e82cd6de_fk_ebay_categories_id"
 FOREIGN KEY ("i2ndCategoryID_id") REFERENCES ebay_categories(id) ON DELETE NO ACTION ;
ALTER TABLE "searching" ADD CONSTRAINT "searching_iEbayCategory_id_9fe370a3_fk_ebay_categories_id"
 FOREIGN KEY ("iEbayCategory_id") REFERENCES ebay_categories(id) ON DELETE NO ACTION ;

human friendly:
select c1."cMarket", c2.name, p."iCategoryID", p."cCatHierarchy"
from category_hierarchies p
left outer join markets c1 on c1."iEbaySiteID" = p."iEbaySiteID_id"
left outer join ebay_categories c2
on c2."iCategoryID" = p."iCategoryID" and c2."iEbaySiteID_id" = p."iEbaySiteID_id"
where p."cCatHierarchy" not like '%' || c2.name ;

the real query:
select p."iCategoryID", p."iEbaySiteID_id", c.name
from category_hierarchies p
left outer join ebay_categories c
on c."iCategoryID" = p."iCategoryID" and c."iEbaySiteID_id" = p."iEbaySiteID_id"
where p."cCatHierarchy" not like '%' || c.name ;

if the queries above find any rows (discrepancy rows)
run on office desktop or on webserver
pms
from ebayinfo.utils import updateCategoryHierarchies
updateCategoryHierarchies()


select * from ebay_categories where "iSupercededBy" is not null ;




'''

# ### after updating ebay categories, check whether         ###
# ### searches that were connected are still connected !!!  ###
# ### (queries above)                                       ###

# ###      if you update categories for a market,           ###
# ###  update sMarketsTable in ebayinfo/tests/__init__.py   ###
# ###    also update the constants just above the table     ###
# ###         best to implement an email reminder           ###

# ### run getWhetherAnyEbayCategoryListsAreUpdated() daily  ###
# from ebayinfo.utils import getWhetherAnyEbayCategoryListsAreUpdated
