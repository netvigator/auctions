

from .utils         import getWhetherAnyEbayCategoryListsAreUpdated
from .utils         import getCategoryListThenStore

from .models        import Market, EbayCategory

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


# ### run getWhetherAnyEbayCategoryListsAreUpdated() daily  ###

