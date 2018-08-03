

from .utils         import getWhetherAnyEbayCategoryListsAreUpdated
from .utils         import getCategoryListThenStore, dSiteID2Market

from .models        import Market, EbayCategory

from core.utils     import getBegTime, sayDuration


# ### l = getWhetherAnyEbayCategoryListsAreUpdated() ###



def getAllMissingCategoryLists():
    #
    oMarkets = Market.objects.all()
    #
    for oMarket in oMarkets:
        #
        bGotThis = EbayCategory.objects.filter( iEbaySiteID = oMarket ).exists()
        #
        if bGotThis:
            #
            print( 'got %s categories already moving on ...' %
                   oMarket.cMarket )
            #
        else:
            #
            getCategoryListThenStore(
                    uMarket         = oMarket,
                    uWantVersion    = oMarket.iCategoryVer,
                    bShowProgress   = True )
            #
            #


def getCategoryListsUpdated( bConsoleOut = False ):
    #
    tBeg = getBegTime( bConsoleOut )
    #
    lNeedUpdates = getWhetherAnyEbayCategoryListsAreUpdated()
    #
    for d in lNeedUpdates:
        #
        getCategoryListThenStore(
                uMarket         = dSiteID2Market[ d['iSiteID'] ],
                uWantVersion    = d['iEbayHas'],
                bShowProgress   = bConsoleOut )
        #
    #
    #
    if bConsoleOut:
        #
        sayDuration( tBeg )


# ### run getWhetherAnyEbayCategoryListsAreUpdated() daily  ###
####  from ebayinfo.tasks import getWhetherAnyEbayCategoryListsAreUpdated, getCategoryListsUpdated
# ### run getCategoryListsUpdated( bConsoleOut = True )     ###
# ### run getCategoryListsUpdated() to update               ###
