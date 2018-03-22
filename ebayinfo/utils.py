from logging                import getLogger

import xml.etree.ElementTree as ET

#from pprint import pprint

from core.utils             import getNamerSpacer
from django.core.exceptions import ObjectDoesNotExist
from django.db              import DataError

from .models                import EbayCategory, Market, CategoryHierarchy

from String.Output          import ReadableNo
from Utils.Progress         import TextMeter, DummyMeter
from Web.HTML               import getChars4HtmlCodes

logger = getLogger(__name__)

class UnexpectedResponse( Exception ): pass

'''
utils for handling info from ebay API 
note the actual calls to the ebay API are in 
core.ebay_wrapper.py
'''

# variable referenced in tests
CATEGORY_VERSION_FILE = '/tmp/Categories_Ver_%s.xml'
CATEGORY_LISTING_FILE = '/tmp/Categories_All_%s.xml'

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


def getTagsValuesGotRoot( root, tTags = tVersionChildTags, sFile = None ):
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


def getCategoryIterable(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117' ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    dTagsValues = getTagsValuesGotRoot(
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



def countCategories(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117',
        bSayCount = False ):
    #
    from String.Output import ReadableNo
    #
    oCategories, dTagsValues = getCategoryIterable( sFile, sWantVersion )
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



def getCategoryDictGenerator(
        sFile = CATEGORY_LISTING_FILE % 'EBAY-US', sWantVersion = '117' ):
    #
    oCategories, dTagsValues = getCategoryIterable( sFile, sWantVersion )
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
categoryDictIterable = getCategoryDictGenerator()
pprint( next( categoryDictIterable ) )
returns
{'CategoryID': '20081',
 'CategoryLevel': '1',
 'CategoryName': 'Antiques',
 'CategoryParentID': '20081',
 'CategoryVersion': '117',
 'LeafCategory': ''}
'''


def putCategoriesInDatabase( sMarket = 'EBAY-US', sWantVersion = '117',
            bShowProgress = False, sFile = None ):
    #
    oMarket = Market.objects.get( cMarket = sMarket )
    #
    # getCategoryDictGenerator checks for the expected version
    #
    if sFile is None:
        #
        sFile = CATEGORY_LISTING_FILE % sMarket
        #
    #
    categoryDictIterable = getCategoryDictGenerator(
        sFile = sFile, sWantVersion = sWantVersion )
    #
    if bShowProgress: # progress meter for running in shell, no need to test
        #
        oProgressMeter = TextMeter()
        #
        print( 'counting categories ...' )
        #
        iCount = 0
        #
        for dCategory in categoryDictIterable: iCount +=1
        #
        categoryDictIterable = getCategoryDictGenerator(
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
            iMarket         = oMarket,
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
            iMarket         = oMarket,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRoot.save()
        #
    iSeq = 0
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
                iMarket         = oMarket, 
                iCategoryID     = int( dCategory['CategoryID'] ) )
            #
        except ObjectDoesNotExist:
            #
            oCategory = EbayCategory(
                iCategoryID     = int( dCategory['CategoryID'] ),
                iMarket         = oMarket )
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
                iMarket     = oMarket, 
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



def getCategoryListThenStore(
            sMarket         = 'EBAY-US',
            sWantVersion    = '118',
            bUseSandbox     = False,
            bShowProgress   = False ):
    #
    from core.ebay_api_calls    import getMarketCategoriesGotGlobalID
    #
    from File.Write             import QuietDump
    from File.Del               import DeleteIfExists
    #
    if bShowProgress: print( 'fetching category list ....' )
    #
    sCategories = getMarketCategoriesGotGlobalID(
            sGlobalID = sMarket, bUseSandbox = bUseSandbox )
    #
    QuietDump( sCategories, CATEGORY_LISTING_FILE % sMarket )
    #
    putCategoriesInDatabase( sMarket = sMarket , sWantVersion = sWantVersion,
            bShowProgress = bShowProgress )



def _getCategoryVersionValues( sFile ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    return getTagsValuesGotRoot( root, sFile = sFile )



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
    from Dict.Get import getReverseDictGotUniqueItems
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
    from core.ebay_api_calls import ( getCategoryVersionGotSiteID,
                                      getCategoryVersionGotGlobalID )
    #
    from File.Write import QuietDump
    from File.Del   import DeleteIfExists
    #
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
    DeleteIfExists( '/tmp', sFile % sGlobalID )
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
    for iSiteID in dSiteID2ListVers:
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
    #
    return lMarketsHaveNewerCategoryVersionLists



def _getCategoryHierarchyID(
            iCategoryID, sCategoryName, iEbaySiteID, dEbayCatHierarchies ):
    #
    tCategoryID = iCategoryID, iEbaySiteID
    
    if tCategoryID in dEbayCatHierarchies:
        #
        iCatHeirarchy = dEbayCatHierarchies[ tCategoryID ]
        #
        bOkCatHeirarchy = CategoryHierarchy.objects.filter( pk = iCatHeirarchy ).exists()
        #
    elif CategoryHierarchy.objects.filter( 
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).exists():
        #
        iCatHeirarchy = CategoryHierarchy.objects.get(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).pk
        #
        dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
        #
    elif EbayCategory.objects.filter(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).exists():
        #
        oEbayCategory   = EbayCategory.objects.get(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID )
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
                sMessage = ( 'For market %s, PARENT of ebay category '
                            '%s does not exist' %
                                ( iEbaySiteID, iCategoryID ) )
                logger.info( sMessage)
                #
                print( sMessage )
                #
                break
                #
            #
            oEbayCategory = oParentCat
            #
        #
        lCatHeirarchy.reverse()
        #
        sCatHeirarchy = '\r'.join( lCatHeirarchy ) # django uses return, but
        # return only does not work in shell, each line overwrites the prior one
        #
        oCategoryHierarchy = CategoryHierarchy(
                iCategoryID     = iCategoryID,
                iMarket         = Market.objects.get(
                                    iEbaySiteID = iEbaySiteID ),
                cCatHierarchy   = sCatHeirarchy )
        #
        oCategoryHierarchy.save()
        #
        iCatHeirarchy = oCategoryHierarchy.pk
        #
        dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
        #
    else: # testing glitch, limited set of categories
        #
        iCatHeirarchy = sCategoryName
        #
        sMessage = ( 'For market %s, ebay category '
                     '%s does not exist' %
                          ( iEbaySiteID, iCategoryID ) )
        logger.info( sMessage)
        #
        print( sMessage )
        #
    #
    return iCatHeirarchy



def getEbayCategoryHierarchies( dItem, dEbayCatHierarchies ):
    #
    ''' return the ebay category hierarchy for a search find item category
    that is, this returns the id of the category hierarchy table row
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
        sCategoryName =    dItem.get( 'secondaryCategory' ).get( 'categoryName' )
        #
        i2ndCatHeirarchy = _getCategoryHierarchyID(
                    i2ndCategoryID, sCategoryName, iEbaySiteID, dEbayCatHierarchies )
        #
    else:
        #
        i2ndCatHeirarchy = None
        #
    #
    return iCatHeirarchy, i2ndCatHeirarchy


    
# ### if any category versions are updated, call            ###
# ### updateMemoryTableUpdated( 'markets', 'iCategoryVer' ) ###
# ###                     in core.utils                     ###


# QuietDump( getCategoryVersionGotGlobalID( 'EBAY-GB' ), 'Categories_Ver_EBAY-GB.xml' )
