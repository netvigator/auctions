
from celery             import shared_task
from celery.schedules   import crontab

from .utils             import getWhetherAnyEbayCategoryListsAreUpdated
from .utils             import getCategoryListThenStore, dSiteID2Market

from .models            import Market, EbayCategory

from core.utils         import getBegTime, sayDuration


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


@shared_task( name = 'ebayinfo.tasks.getCategoryListThenStore' )
def getCategoryListThenStoreTask(
                uMarket         = dSiteID2Market[ d['iSiteID'] ],
                uWantVersion    = d['iEbayHas'],
                bShowProgress   = False )
    #
    getCategoryListThenStore(
            uMarket         = uMarket,
            uWantVersion    = uWantVersion,
            bShowProgress   = bShowProgress )
    #



def getCategoryListsUpdated( bConsoleOut = False ):
    #
    tBeg = getBegTime( bConsoleOut )
    #
    lNeedUpdates = getWhetherAnyEbayCategoryListsAreUpdated()
    #
    for d in lNeedUpdates:
        #
        getCategoryListThenStoreTask.delay(
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