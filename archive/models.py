from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

from django.contrib.auth        import get_user_model

User = get_user_model()



class Item(models.Model):
    iItemNumb       = models.BigIntegerField( 'ebay item number',
                        primary_key = True )
    cDescription    = models.TextField( 'description' )
    bBestOfferable  = models.BooleanField( 'buy it now enabled?',
                        default = False )
    tTimeBeg        = models.DateTimeField( 'beginning date/time',null=True )
    tTimeEnd        = models.DateTimeField( 'ending date/time',   null=True )
    cEbayItemURL    = models.CharField( 'ebay item URL', max_length =188 )
    cListingType    = models.CharField( 'listing type', max_length = 15 )
    cLocation       = models.CharField( 'location', max_length = 48 )
    cPaymentMethods = models.CharField( 'ebay item URL', max_length = 88 )
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88, null = True, blank = True )
    cPictureURLs    = models.TextField( 'picture URLs',
                        null = True, blank = True )
    cPostalCode     = models.CharField( 'postal code', max_length = 12 )
    iCategoryID     = models.PositiveIntegerField( 'primary category ID',
                        null = True )
    cCategory       = models.CharField( 'primary category',
                        max_length = 48 )
    iQuantity       = models.SmallIntegerField( 'quantity' )
    cSellerID       = models.CharField( 'seller user name', max_length = 48 )
    iFeedbackScore  = models.SmallIntegerField( 'seller feedback score' )
    cFeedbackPercent= models.CharField( 'seller feedback percent', max_length = 8 )
    iBidCount       = models.SmallIntegerField( 'bid count' )
    dCurrentPrice   = models.DecimalField( # form was throwing nonsense error
                        'current price (converted)', # for MoneyField
                        max_digits=10, decimal_places=2,    # but not for
                        db_index = False )                  # DecimalField
    dConvertCurrency= models.CharField( 'local currency converted to this',
                        max_length = 3, default = 'USD' )
    lCurrentPrice   = models.DecimalField( 'current price (local currency)',
                        max_digits = 10, decimal_places = 2,
                        null = True )
    lLocalCurrency  = models.CharField( 'local currency',
                        max_length = 3, default = 'USD' )
    cHighBidder     = models.CharField( 'high bidder user name', max_length = 48 )
    cListingStatus  = models.CharField( 'Listing Status', max_length = 18 )
    iQuantitySold   = models.SmallIntegerField( 'quantity sold' )
    cShipToLocations= models.CharField( 'ship to locations', max_length =188 )
    cSite           = models.CharField( 'Site', max_length = 8 )
    cTimeLeft       = models.CharField( 'time left', max_length =18 )
    cTitle          = models.CharField( 'item title',
                        max_length = 80 )
    iHitCount       = models.SmallIntegerField( 'Hit Count' )
    cCategoryPath   = models.CharField( 'category path', max_length = 48 )
    cCountry        = CountryField( "Country" )
    cReturnPolicy   = models.CharField( 'Return Policy', max_length = 48 )
    dMinimumBid     = models.DecimalField( 'Minimum Bid',
                        max_digits = 6, decimal_places = 2, null = True )
    cBidCurrency    = models.CharField( 'bid currency',
                        max_length = 3, default = 'USD' )
    iConditionID    = models.SmallIntegerField( 'Condition ID',
                        null = True, blank = True )
    cCondition      = models.CharField( 'condition display name',
                        max_length = 28, null = True, blank = True )
    bGlobalShipping = models.BooleanField( 'Global Shipping', default=False )

    tCreate         = models.DateTimeField( 'created on',
                        db_index = True, auto_now_add= True )


    def __str__(self):
        return self.iItemNumb

    class Meta:
        verbose_name_plural = 'items'
        db_table            = verbose_name_plural



class ItemImage(models.Model):
    iItemNumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    isequence       = models.PositiveSmallIntegerField( 'sequence' )
    cfilename       = models.CharField( 'local file name', max_length = 28 )
    coriginalurl    = models.TextField( 'original URL' )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    def __str__(self):
        return self.iItemNumb

    class Meta:
        verbose_name_plural = 'itemimages'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'isequence',)
#
