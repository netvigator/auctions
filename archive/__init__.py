from core.utils     import getDateTimeObjGotEbayStr, getShrinkItemURL

from archive.utils  import getListAsLines, getListWithCommas # in __init__.py

from Utils.Config   import getBoolOffYesNoTrueFalse


d = dict

dItemFields = d(
    iItemNumb       = d( t = ( "ItemID",),
                         f = int ),
    cDescription    = d( t = ( "Description",), ),
    bBestOfferable  = d( t = ( "BestOfferEnabled",),
                         f = getBoolOffYesNoTrueFalse ),
    tTimeEnd        = d( t = ( "EndTime",),
                         f = getDateTimeObjGotEbayStr ),
    tTimeBeg        = d( t = ( "StartTime",),
                         f = getDateTimeObjGotEbayStr ),
    cEbayItemURL    = d( t = ( "ViewItemURLForNaturalSearch",),
                         f = getShrinkItemURL ),
    cListingType    = d( t = ( "ListingType",), ),
    cLocation       = d( t = ( "Location",), ),
    cPaymentMethods = d( t = ( "PaymentMethods",),
                         f = getListWithCommas ),
    cGalleryURL     = d( t = ( "GalleryURL",), ),
    cPictureURLs    = d( t = ( "PictureURL",),
                         f = getListAsLines ),
    cPostalCode     = d( t = ( "PostalCode",), ),
    iCategoryID     = d( t = ( "PrimaryCategoryID",),
                         f = int ),
    cCategoryID     = d( t = ( "PrimaryCategoryName",), ),
    iQuantity       = d( t = ( "Quantity",),
                         f = int ),
    cSellerID       = d( t = ( "Seller", "UserID",), ),
    iFeedbackScore  = d( t = ( "Seller", "FeedbackScore",),
                         f = int ),
    cFeedbackPercent= d( t = ( "Seller", "PositiveFeedbackPercent",), ),
    iBidCount       = d( t = ( "BidCount",),
                         f = int ),
    dCurrentPrice   = d( t = ( "ConvertedCurrentPrice", "Value",),
                         f = float ),
    dConvertCurrency= d( t = ( "ConvertedCurrentPrice", "CurrencyID",), ),
    lCurrentPrice   = d( t = ( "CurrentPrice", "Value",),
                         f = float ),
    lLocalCurrency  = d( t = ( "CurrentPrice", "CurrencyID",), ),
    cHighBidder     = d( t = ( "HighBidder", "UserID",), ),
    cListingStatus  = d( t = ( "ListingStatus",), ),
    iQuantitySold   = d( t = ( "QuantitySold",),
                         f = int ),
    cShipToLocations= d( t = ( "ShipToLocations",),
                         f = getListWithCommas ),
    cSite           = d( t = ( "Site",), ),
    cTimeLeft       = d( t = ( "TimeLeft",), ),
    cTitle          = d( t = ( "Title",), ),
    iHitCount       = d( t = ( "HitCount",),
                         f = int ),
    cCategoryPath   = d( t = ( "PrimaryCategoryIDPath",), ),
    cCountry        = d( t = ( "Country",), ),
    cReturnPolicy   = d( t = ( "ReturnPolicy", "ReturnsAccepted",), ),
    dMinimumBid     = d( t = ( "MinimumToBid", "Value",), ),
    cBidCurrency    = d( t = ( "MinimumToBid", "CurrencyID",), ),
    iConditionID    = d( t = ( "ConditionID",),
                         f = int ),
    cCondition      = d( t = ( "ConditionDisplayName",), ),
    bGlobalShipping = d( t = ( "GlobalShipping",),
                         f = getBoolOffYesNoTrueFalse ) )


