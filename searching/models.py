from django.db                  import models
from django_countries.fields    import CountryField
from django.urls                import reverse

from core.models                import IntegerRangeField
from core.utils                 import getReverseWithUpdatedQuery

from models.models              import Model
from brands.models              import Brand
from categories.models          import Category

from ebayinfo.models            import CategoryHierarchy, Market, EbayCategory

from django.contrib.auth        import get_user_model
User = get_user_model()

from searching                  import EBAY_SHIPPING_CHOICES

from ebayinfo.models            import EbayCategory

from Time.Output                import getIsoDateTimeFromDateTime


# ### models can be FAT but not too FAT! ###



class Search(models.Model):
    cTitle          = models.CharField( 'short description',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'search for key words (maximum length 350 characters)',
        max_length = 350, null = True, blank = True,
        help_text = 'What you type here will go into the ebay serch box '
                    '-- mulitple terms will result in an AND search.  '
                    'TIPS: to exclude words, put a - in front '
                    '(without any space), '
                    'search for red OR green handbags as follows: '
                    'handbags (red,green)  search for handbags but '
                    'exclude red and green as follows: '
                    'handbags -(red,green)  350 characters MAX' )
    # max length for a single key word is 98
    #models.ForeignKey( EbayCategory, models.PositiveIntegerField(
    iEbayCategory   = models.ForeignKey( EbayCategory,
                        verbose_name = 'ebay category (optional)',
                        null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!) '
                    '(Both are OK)', on_delete=models.CASCADE )
    iDummyCategory  = models.PositiveIntegerField( 'ebay category number',
                                null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!)' )
    cPriority       = models.CharField( 'processing priority',
                                max_length = 2, null = True,
                                choices = (),
        help_text = 'high priority A1 A2 A3 ... Z9 low priority' )
    tBegSearch      = models.DateTimeField( 'last search started',
                                           null = True )
    tEndSearch      = models.DateTimeField( 'last search completed',
                                           null = True )
    cLastResult     = models.TextField( 'last search outcome', null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                            on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )

    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'searches'
        db_table        = 'searching'
        unique_together = ( ( 'iUser',      'cPriority' ),
                            ( 'iUser',      'cTitle'    ),
                            ( 'iUser',      'cKeyWords',   'iEbayCategory',) )
        ordering        = ('cTitle',)

    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'searching:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )


# Item IDs are unique across all eBay sites
# http://developer.ebay.com/devzone/shopping/docs/callref/getsingleitem.html

class ItemFound(models.Model):

    EBAY_SHIPPING_CHOICES = EBAY_SHIPPING_CHOICES

    iItemNumb       = models.BigIntegerField( 'ebay item number',
                        primary_key = True )
    cTitle          = models.CharField( 'item title',     max_length = 80 )
    cSubTitle       = models.CharField( 'item sub title', max_length = 80,
                        null = True, blank = True )
    cLocation       = models.CharField( 'location',
                        max_length = 48 )
    cCountry        = CountryField( "country" )
    cMarket         = models.CharField( 'market Global ID',
                        max_length = 14 )
    iEbaySiteID     = models.ForeignKey( Market,
                        verbose_name = 'ebay site ID (PK)', db_index=True,
                        on_delete=models.CASCADE )
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88, null = True, blank = True )
    cEbayItemURL    = models.CharField( 'ebay item URL',
                        max_length =188 )
    tTimeBeg        = models.DateTimeField( 'beginning date/time',null=True )
    tTimeEnd        = models.DateTimeField( 'ending date/time',   null=True )
    bBestOfferable  = models.BooleanField(
                        'best offer enabled?', default = False )
    bBuyItNowable   = models.BooleanField(
                        'buy it now enabled?',default = False )
    cListingType    = models.CharField(
                        'listing type', max_length = 15 )
    lLocalCurrency  = models.CharField(
                        'local currency', max_length = 3, default = 'USD' )
    lCurrentPrice   = models.DecimalField( 'current price',
                        max_digits = 10, decimal_places = 2,
                        null = True, blank = True )      # use DecimalField not MoneyField
    dCurrentPrice   = models.DecimalField( # form was throwing nonsense error
                        'current price (converted to USD)', # for MoneyField
                        max_digits=10, decimal_places=2,    # but not for
                        db_index = False )                  # DecimalField
    iShippingType   = models.PositiveSmallIntegerField(
                        'shipping type',
                        choices = EBAY_SHIPPING_CHOICES,
                        null = True ) # data prior to Feb 2019 d/n have
    iCategoryID     = models.ForeignKey( EbayCategory,
                        verbose_name = 'primary category ID',
                        related_name = 'ebay_primary_category',
                        on_delete=models.CASCADE,
                        null = True, blank = True ) # need for testing
    cCategory       = models.CharField( 'primary category',
                        max_length = 48 )
    iCatHeirarchy   = models.ForeignKey( CategoryHierarchy,
                        verbose_name = 'category hierarchy (primary)',
                        related_name = 'primary_category',
                        null = True, blank = True, on_delete=models.CASCADE )
    i2ndCategoryID  = models.ForeignKey( EbayCategory,
                        verbose_name = 'secondary category ID (optional)',
                        related_name = 'ebay_secondary_category',
                        null = True, blank = True )
    c2ndCategory    = models.CharField( 'secondary category (optional)',
                        max_length = 48, null = True, blank = True )
    i2ndCatHeirarchy= models.ForeignKey( CategoryHierarchy,
                        verbose_name = 'category hierarchy (secondary)',
                        related_name = 'secondary_category',
                        null = True, blank = True, on_delete=models.CASCADE )

    # condition is optional but may become required in the future
    # https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html
    iConditionID    = models.IntegerField( 'condition ID',
                                         null = True, blank = True )
    cCondition      = models.CharField( 'condition display name',
                        max_length = 28, null = True, blank = True )

    cSellingState   = models.CharField( 'selling state',
                        max_length = 18 )
    bCancelledItem  = models.BooleanField(
                        'Invalid Or Non-Existent Item Number',default = False )
    tCreate         = models.DateTimeField( 'created on',
                        db_index = True, auto_now_add= True )
    tRetrieved      = models.DateTimeField( 'retrieved info',
                        null = True, blank = True )
    tRetrieveFinal  = models.DateTimeField( 'retrieved info after end',
                        null = True, blank = True )


    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'itemsfound'
        db_table            = verbose_name_plural



class UserItemFound(models.Model):
    iItemNumb       = models.ForeignKey( ItemFound, on_delete=models.CASCADE )
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
    bListExclude    = models.BooleanField( 'exclude from listing?',
                        default = False )
    tGotPics        = models.DateTimeField( 'got pictures',
                        null = True, blank = True )
    bAuction        = models.BooleanField(
                        'Auction or Auction with Buy It Now',default = False )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                        on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', db_index = True )
    tModify         = models.DateTimeField( 'updated on', auto_now = True )
    tRetrieved      = models.DateTimeField( 'retrieved info',
                        null = True, blank = True )
    tRetrieveFinal  = models.DateTimeField( 'retrieved info after end',
                        null = True, blank = True )

    def __str__(self):
        return self.iItemNumb.cTitle

    class Meta:
        verbose_name_plural = 'useritemsfound'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'iUser', 'iModel', 'iBrand' )

    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'searching:item_found_detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )



class ItemFoundTemp(models.Model):
    iItemNumb       = models.ForeignKey( ItemFound, on_delete=models.CASCADE )
    iHitStars       = IntegerRangeField(
                        'hit stars', null = True,
                        min_value = 0, max_value = 1000, default = 0 )
    iSearch         = models.ForeignKey( Search,
                        verbose_name = 'Search that first found this item',
                        on_delete=models.CASCADE )
    iModel          = models.ForeignKey( Model,     null = True,
                        on_delete=models.CASCADE )
    iBrand          = models.ForeignKey( Brand,     null = True,
                        on_delete=models.CASCADE )
    iCategory       = models.ForeignKey( Category,  null = True,
                        on_delete=models.CASCADE )
    iStarsModel     = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )
    iStarsBrand     = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )
    iStarsCategory  = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )

    iFoundModelLen  = models.PositiveSmallIntegerField( default = 0 )

    cWhereCategory  = models.CharField( 'where category was found',
                        default = 'title',
                        max_length = 10 ) # title heirarchy1 heirarchy2

    def __str__(self):
        return 'ItemFound - %s' % self.iItemNumb

    class Meta:
        verbose_name_plural = 'itemsfoundtemp'
        db_table            = verbose_name_plural


class SearchLog(models.Model):
    iSearch     = models.ForeignKey( Search,
                        verbose_name = 'Search that first found this item',
                        on_delete=models.CASCADE )
    tBegSearch  = models.DateTimeField( 'search started',
                        db_index = True )
    tEndSearch  = models.DateTimeField( 'search completed',
                        null = True )
    tBegStore   = models.DateTimeField( 'processing started',
                        null = True )
    tEndStore   = models.DateTimeField( 'processing completed',
                        null = True )
    iItems      = models.PositiveIntegerField( 'items found',
                        null = True )
    iStoreItems = models.PositiveIntegerField( 'items stored',
                        null = True )
    iStoreUsers = models.PositiveIntegerField( 'stored for owner',
                        null = True )
    iItemHits   = models.PositiveIntegerField(
                        'have category, brand & model',
                        null = True )
    cResult     = models.TextField( 'search outcome', null = True )

    def __str__(self):
        return '%s - %s' % (
            getIsoDateTimeFromDateTime( self.tBegSearch ),
            self.iSearch.cTitle )

    class Meta:
        verbose_name_plural = 'searchlogs'
        db_table            = verbose_name_plural


