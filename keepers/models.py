from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

from django.contrib.auth        import get_user_model

User = get_user_model()



class Keeper(models.Model):
    iItemNumb       = models.BigIntegerField( 'ebay item number',
                        primary_key = True )
    cDescription    = models.TextField( 'description',
                        null = True, blank = True ) # d/n always get
    bBestOfferable  = models.BooleanField( 'buy it now enabled?',
                        default = False )
    tTimeBeg        = models.DateTimeField( 'beginning date/time',null=True )
    tTimeEnd        = models.DateTimeField( 'ending date/time',   null=True )
    cEbayItemURL    = models.CharField( 'ebay item URL', max_length =188 )
    cListingType    = models.CharField( 'listing type', max_length = 15 )
    cLocation       = models.CharField( 'location', max_length = 48 )
    cPaymentMethods = models.CharField( 'ebay item URL',
                        max_length = 88, null = True, blank = True )
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88, null = True, blank = True )
    cPictureURLs    = models.TextField( 'picture URLs',
                        null = True, blank = True )
    cPostalCode     = models.CharField( 'postal code', max_length = 12,
                        null = True, blank = True )
    iCategoryID     = models.PositiveIntegerField( 'primary category ID',
                        null = True, blank = True )
    cCategory       = models.CharField( 'primary category',
                        max_length = 48 )
    iQuantity       = models.SmallIntegerField( 'quantity' )
    cSellerID       = models.CharField( 'seller user name', max_length = 48 )
    iFeedbackScore  = models.BigIntegerField( 'seller feedback score',
                        null = True, blank = True )
    cFeedbackPercent= models.CharField( 'seller feedback percent', max_length = 8 )
    iBidCount       = models.SmallIntegerField( 'bid count' )
    dConvertPrice   = models.DecimalField( # form was throwing nonsense error
                        'price (converted)',        # for MoneyField
                        max_digits=10, decimal_places=2,    # but not for
                        db_index = False )                  # DecimalField
    cConvertCurrency= models.CharField( 'local currency converted to this',
                        max_length = 3, default = 'USD' )
    lLocalPrice     = models.DecimalField( 'price (local currency)',
                        max_digits = 10, decimal_places = 2,
                        null = True, blank = True )
    lLocalCurrency  = models.CharField( 'local currency',
                        max_length = 3, default = 'USD' )
    cHighBidder     = models.CharField( 'high bidder user name',
                        max_length = 48, null = True, blank = True )
    cListingStatus  = models.CharField( 'Listing Status', max_length = 18 )
    iQuantitySold   = models.SmallIntegerField( 'quantity sold' )
    cShipToLocations= models.TextField( 'ship to locations' )
    cSite           = models.CharField( 'Site', max_length = 14 )
    cTimeLeft       = models.CharField( 'time left', max_length =18 )
    cTitle          = models.CharField( 'item title',
                        max_length = 80 )
    iHitCount       = models.SmallIntegerField( 'Hit Count',
                        null = True, blank = True ) # ebay d/n always include
    cCategoryIDs    = models.CharField( 'category IDs',   max_length =  88 )
    cCategoryNames  = models.CharField( 'category names', max_length = 148 )
    cCountry        = CountryField( "Country" )
    cReturnPolicy   = models.CharField( 'Return Policy', max_length = 48 )
    dMinimumBid     = models.DecimalField( 'Minimum Bid',
                        max_digits = 12, decimal_places = 2,
                        null = True, blank = True )
    cBidCurrency    = models.CharField( 'bid currency',
                        max_length = 3, default = 'USD',
                        null = True, blank = True )
    iConditionID    = models.SmallIntegerField( 'Condition ID',
                        null = True, blank = True )
    cCondition      = models.CharField( 'condition display name',
                        max_length = 28, null = True, blank = True )
    bGlobalShipping = models.BooleanField( 'Global Shipping', default=False )

    bBuyItNowable   = models.BooleanField(
                        'buy it now enabled?',default = False )
    lBuyItNowPrice  = models.DecimalField( 'buy it now price (local currency)',
                        max_digits = 10, decimal_places = 2,
                        null = True, blank = True )
    lBuyItNowCurrenc= models.CharField( 'buy it now local currency',
                        max_length = 3, default = 'USD',
                        null = True, blank = True )
    dBuyItNowPrice  = models.DecimalField(
                        'buy it now price (converted)',
                        max_digits=10, decimal_places=2,
                        null = True, blank = True )
    cBuyItNowConvert= models.CharField(
                        'buy it now local currency converted to this',
                        max_length = 3, default = 'USD',
                        null = True, blank = True )

    tCreate         = models.DateTimeField( 'created on',
                        db_index = True, auto_now_add= True )

    tModify         = models.DateTimeField( 'updated on', null = True )

    bGotPictures    = models.BooleanField( 'pictures downloaded?',
                        default = False )
    tGotPictures    = models.DateTimeField( 'pictures downloaded',
                        null = True )
    iGotPictures    = models.PositiveSmallIntegerField(
                        'how many pictures downloaded',
                        null = True, blank = True )

    def __str__(self):
        return str( self.iItemNumb )

    class Meta:
        verbose_name_plural = 'keepers'
        db_table            = verbose_name_plural

    def get_absolute_url(self):
        #
        return getReverse(
                'keepers:detail',
                kwargs = { 'pk': self.pk } )
#


class KeeperImage(models.Model):
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
        verbose_name_plural = 'keeperimages'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'isequence',)
#
