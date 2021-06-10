
# from celery           import shared_task

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


'''
@shared_task( name = 'ebayinfo.tasks.getCategoryListThenStore' )
def getCategoryListThenStoreTask( uMarket, uWantVersion, bShowProgress ):
    #
    getCategoryListThenStore(
            uMarket         = uMarket,
            uWantVersion    = uWantVersion,
            bShowProgress   = bShowProgress )
    #
'''

# ### use the function of the SAME NAME in utils ###
# ### use the function of the SAME NAME in utils ###
# ### use the function of the SAME NAME in utils ###
# ### use the function of the SAME NAME in utils ###
'''
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
        # getCategoryListThenStoreTask.apply_async(
        #     queue='low_priority', kwargs = {
        #         uMarket         : dSiteID2Market[ d['iSiteID'] ],
        #         uWantVersion    : d['iEbayHas'],
        #         bShowProgress   : bConsoleOut } )
        #
    #
    #
    if bConsoleOut:
        #
        sayDuration( tBeg )
'''


# ### on a separate machine and database, no need for celery !!! ###
# ### on a separate machine and database, no need for celery !!! ###
# ### on a separate machine and database, no need for celery !!! ###
# ### on a separate machine and database, no need for celery !!! ###

# ### run getWhetherAnyEbayCategoryListsAreUpdated() daily  ###
# ### python manage.py test ebayinfo.tests.test_utils.MarketsAndCategoriesTests
# ### from ebayinfo.tasks import getCategoryListsUpdated    ###
# ### run getCategoryListsUpdated( bConsoleOut = True )     ###
# ### run getCategoryListsUpdated() to update               ###

# ### step by step instructions at bottom of ./utils.py     ###
