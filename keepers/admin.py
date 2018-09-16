from django.contrib import admin

# Register your models here.

from .models import Keeper

class KeeperAdmin(admin.ModelAdmin):
    list_display = (
        "iItemNumb",
        "cDescription",
        "bBestOfferable",
        "tTimeBeg",
        "tTimeEnd",
        "cEbayItemURL",
        "cListingType",
        "cLocation",
        "cPaymentMethods",
        "cGalleryURL",
        "cPictureURLs",
        "cPostalCode",
        "iCategoryID",
        "cCategory",
        "iQuantity",
        "cSellerID",
        "iFeedbackScore",
        "cFeedbackPercent",
        "iBidCount",
        "dConvertPrice",
        "cConvertCurrency",
        "lLocalPrice",
        "lLocalCurrency",
        "cHighBidder",
        "cListingStatus",
        "iQuantitySold",
        "cShipToLocations",
        "cSite",
        "cTimeLeft",
        "cTitle",
        "iHitCount",
        "cCategoryIDs",
        "cCategoryNames",
        "cCountry",
        "cReturnPolicy",
        "dMinimumBid",
        "cBidCurrency",
        "iConditionID",
        "cCondition",
        "bGlobalShipping",
        "bBuyItNowable",
        "lBuyItNowPrice",
        "lBuyItNowCurrenc",
        "dBuyItNowPrice",
        "cBuyItNowConvert",
        "tCreate",
        "tModify",
        "bGotPictures",
        "tGotPictures",
        "iGotPictures" )



admin.site.register( Keeper, KeeperAdmin )
