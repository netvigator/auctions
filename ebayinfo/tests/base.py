from core.tests.base_class  import TestCasePlus
from django_webtest         import WebTest

from ..models               import Market, EbayCategory

from ebayinfo.tests         import sMarketsTable, \
                                   EBAY_CURRENT_VERSION_US, \
                                   EBAY_CURRENT_VERSION_GB, \
                                   EBAY_CURRENT_VERSION_Mo, \
                                   EBAY_CURRENT_VERSION_ENCA, \
                                   sEbayCategoryDump

from ebayinfo.tests.utils   import getMarketsDict

from pyPks.Utils.Config     import getBoolOffYesNoTrueFalse as getBool
from pyPks.Utils.DataBase   import getTableFromScreenCaptureGenerator


dMarkets = getMarketsDict( sMarketsTable )


class PutMarketsInDatabaseMixIn( object ):

    @classmethod
    def setUpTestData( cls ):
        #
        '''fetches the markets table text dump,
        uses that to populate the markets table.
        useful for testing, where the database starts empty.'''
        #
        super().setUpTestData()
        #
        for k, v in dMarkets.items():
            #
            oMarket = Market(
                iEbaySiteID     = k,
                cMarket         = v.cMarket,
                cCountry        = v.cCountry,
                iCategoryVer    = v.iCategoryVer,
                cLanguage       = v.cLanguage,
                bHasCategories  = v.bHasCategories,
                cCurrencyDef    = v.cCurrencyDef,
                iUtcPlusOrMinus = v.iUtcPlusOrMinus,
                cUseCategoryID  = v.cUseCategoryID )
            #
            oMarket.save()
        #
        cls.iCategories = 0
        #
        cls.market = Market.objects.get( pk = 0 )



class PutMarketsInDatabaseTestPlusBase( PutMarketsInDatabaseMixIn, TestCasePlus ):
    ''' set up for tests '''
    #
    # compatible with new June 2021
    #
    pass


class PutMarketsInDatabaseWebTestBase( PutMarketsInDatabaseMixIn, WebTest ):
    ''' set up for tests '''
    #
    pass


class GetEbayCategoriesMixIn( object ):
    #
    '''new June 2021'''
    #
    @classmethod
    def setUpTestData( cls ):
        #
        super().setUpTestData()
        #
        sMarket, sWantVersion = 'EBAY-US', EBAY_CURRENT_VERSION_US
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID     = cls.market,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-GB', EBAY_CURRENT_VERSION_GB
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 3, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-ENCA', EBAY_CURRENT_VERSION_ENCA
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 2, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-MOTOR', EBAY_CURRENT_VERSION_Mo
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 100, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sEbayCategoryDump )
        #
        tHeader = next( oTableIter )
        #
        iCategories = 0
        #
        setTestCategories = set( [] )
        #
        oPriorRoot = oRootCategory
        #
        dCategoryEbaySiteIDs = {}
        #
        for lParts in oTableIter:
            #
            iCategoryID             = int( lParts[1] )
            iParentOfThis           = int( lParts[4] )
            iThisLevel              = int( lParts[3] )
            iEbaySiteID             = int( lParts[7] )
            #
            if EbayCategory.objects.filter(
                        iCategoryID     = iCategoryID,
                        iEbaySiteID_id  = iEbaySiteID ).exists():
                #
                print('for market %s, iCategoryID already exists: %s -- '
                    'clean up the list!' % (lParts[7],lParts[1] ) )
                #
                continue
                #
            #
            setTestCategories.add( ( iEbaySiteID, iCategoryID ) )
            #
            oCategory = EbayCategory(
                    iCategoryID     =           iCategoryID,
                    name            =           lParts[2],
                    iLevel          =           iThisLevel,
                    bLeafCategory   = getBool(  lParts[5] ),
                    iTreeVersion    = int(      lParts[6] ),
                    iEbaySiteID_id  =           iEbaySiteID )
            #
            if iThisLevel == 1: # top level iParentID
                #
                if oPriorRoot.iEbaySiteID_id != iEbaySiteID:
                    #
                    oRootCategory = EbayCategory.objects.get(
                        iEbaySiteID_id  = iEbaySiteID,
                        iLevel          = 0 )
                    #
                    oPriorRoot = oRootCategory
                    #
                #
                oCategory.iParentID = oRootCategory.iCategoryID
                oCategory.parent    = oRootCategory
                #
            else:
                #
                oParent         = EbayCategory.objects.get(
                                        iCategoryID     = iParentOfThis,
                                        iEbaySiteID_id  = iEbaySiteID )
                #
                oCategory.iParentID = iParentOfThis
                #
                bGotCategory4Market = False
                #
                bGotCategory4Market = (
                        ( iParentOfThis, iEbaySiteID )
                        in
                        dCategoryEbaySiteIDs )
                #
                if bGotCategory4Market:
                    #
                    iParentID = dCategoryEbaySiteIDs[ ( iParentOfThis, iEbaySiteID ) ]
                    #
                    oCategory.parent_id = iParentID
                    #
                else:
                    #
                    print('in market %s, cannot find iCategoryID %s, '
                          'parent of iCategoryID %s' %
                          ( lParts[7], lParts[4], lParts[1] ) )
                #
            #
            oCategory.save()
            #
            dCategoryEbaySiteIDs[ ( iCategoryID, iEbaySiteID ) ] = oCategory.id
            #
            iCategories += 1
            #
        #
        cls.iCategories = iCategories + 4 # add root categories
        #
        cls.setTestCategories = frozenset( setTestCategories )
        #


class GetMarketsAndCategoriesWebTestSetUp(
        GetEbayCategoriesMixIn, PutMarketsInDatabaseWebTestBase ):
    #
    '''new June 2021'''
    #
    pass



class GetMarketsAndCategoriesTestPlusSetUp(
        GetEbayCategoriesMixIn, PutMarketsInDatabaseTestPlusBase ):
    #
    #
    '''new June 2021'''
    #
    pass

