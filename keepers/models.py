from django.db                  import models
from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse

from django_countries.fields    import CountryField

from core.models                import IntegerRangeField

from finders                    import EBAY_SHIPPING_CHOICES

from models.models          import Model
from brands.models          import Brand
from categories.models      import Category

from searching.models           import Search

# not sure this is needed
User = get_user_model()



class Keeper( models.Model ):

    EBAY_SHIPPING_CHOICES = EBAY_SHIPPING_CHOICES

    iItemNumb       = models.BigIntegerField( 'item number',
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
    cPaymentMethods = models.CharField( 'Payment methods',
                        max_length = 88, null = True, blank = True )
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88, null = True, blank = True )
    cPictureURLs    = models.TextField( 'picture URLs',
                        null = True, blank = True )
    cPostalCode     = models.CharField( 'postal code', max_length = 12,
                        null = True, blank = True )
    iCategoryID     = models.PositiveIntegerField( 'primary category ID',
                        null = True, blank = True )
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
    iShippingType   = models.PositiveSmallIntegerField(
                        'shipping type',            # not in result info
                        choices = EBAY_SHIPPING_CHOICES,
                        null = True, blank = True ) # comes from item found
    bGlobalShipping = models.BooleanField( 'Global Shipping', default=False )
    bBuyItNowable   = models.NullBooleanField(
                        'buy it now enabled?', default = False,
                        null = True, blank = True )
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
    tRetrieved      = models.DateTimeField( 'retrieved info',
                        null = True, blank = True )
    tRetrieveFinal  = models.DateTimeField( 'retrieved info after end',
                        null = True, blank = True )

    def __str__(self):
        return str( self.iItemNumb )

    class Meta:
        verbose_name_plural = 'keepers'
        db_table            = verbose_name_plural

    def getUsersForKeeper( self, oKeeper, request ):
        #
        oUser = request.user
        #
        qsUserItems = UserKeeper.objects.filter(
                        iUser       = oUser,
                        iItemNumb   = oKeeper.iItemNumb
                    ).order_by( '-iHitStars' )
        #
        return qsUserItems

    def get_absolute_url(self):
        #
        return reverse( 'keepers:detail', kwargs = { 'pk': self.pk } )
#


class UserKeeper(models.Model):
    iItemNumb       = models.ForeignKey( Keeper, on_delete=models.PROTECT )
    iHitStars       = IntegerRangeField(
                        'hit stars', null = True, db_index = True,
                        min_value = 0, max_value = 1000, default = 0 )
    bGetPictures    = models.BooleanField( 'get description & pictures?',
                        default = False )
    tLook4Hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    iSearch         = models.ForeignKey( Search,
                        verbose_name = 'Search that first found this item',
                        on_delete=models.CASCADE )
    iModel          = models.ForeignKey( Model,    null = True, blank = True,
                        verbose_name = 'Model Name/Number',
                        on_delete=models.CASCADE )
    iBrand          = models.ForeignKey( Brand,    null = True, blank = True,
                        verbose_name = 'Brand',
                        on_delete=models.CASCADE )
    iCategory       = models.ForeignKey( Category, null = True, blank = True,
                        verbose_name = 'Category',
                        on_delete=models.CASCADE )
    cWhereCategory  = models.CharField( 'where category was found',
                        default = 'title',
                        max_length = 10 ) # title heirarchy1 heirarchy2
    # bListExclude  = models.BooleanField( 'exclude from listing?',
    #                   default = False )
    # tGotPics      = models.DateTimeField( 'got pictures',
    #                   null = True, blank = True )
    bAuction        = models.BooleanField(
                        'Auction or Auction with Buy It Now',default = False )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                        on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', db_index = True )
    tModify         = models.DateTimeField( 'updated on', auto_now = True )

    #
    # more normalized to store this info in keepers only -- OK?
    # tRetrieved    = models.DateTimeField( 'retrieved info',
    #                   null = True, blank = True )
    # tRetrieveFinal= models.DateTimeField( 'retrieved info after end',
    #                   null = True, blank = True )

    def __str__(self):
        return self.iItemNumb.cTitle

    class Meta:
        verbose_name_plural = 'userkeepers'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'iUser', 'iModel', 'iBrand' )

    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'keepers:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )






class KeeperImage(models.Model):
    iItemNumb       = models.BigIntegerField(
                        'item number', primary_key = True )
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
