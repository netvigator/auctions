from django.db                  import models
from django_countries.fields    import CountryField
from django.urls                import reverse

from models.models              import Model
from brands.models              import Brand
from categories.models          import Category

from ebayinfo.models            import CategoryHierarchy, Market

# Create your models here.

from django.contrib.auth        import get_user_model
User = get_user_model()

# not working: from django.utils.safestring import mark_safe

from core.utils                 import getReverseWithUpdatedQuery

from ebayinfo.models            import EbayCategory

class Search(models.Model):
    cTitle          = models.CharField( 'short description',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'search for key words (maximum length 350 characters)',
        max_length = 350, null = True, blank = True,
        help_text = 'Bot will search for these words in the auction titles '
                    '-- (key words OR ebay category required!) '
                    '(Including both is OK)' )
    # max length for a single key word is 98
    #models.ForeignKey( EbayCategory, models.PositiveIntegerField(
    iEbayCategory   = models.ForeignKey( EbayCategory,
                        verbose_name = 'ebay category (optional)',
                        null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!) '
                    '(Both are OK)' )
    iDummyCategory  = models.PositiveIntegerField( 'ebay category number',
                                null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!)' )
    cPriority       = models.CharField( 'processing priority',
                                max_length = 2, null = True,
        help_text = 'high priority 1 ... 9 A ... Z a ... z low priority' )
    tSearchStarted  = models.DateTimeField( 'last search started',
                                           null = True )
    tSearchComplete = models.DateTimeField( 'last search completed',
                                           null = True )
    cLastResult     = models.CharField( 'last search outcome',
                                max_length = 28, null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
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
    iItemNumb       = models.BigIntegerField( 'ebay item number',
                        primary_key = True )
    cTitle          = models.CharField(
                        'auction title', max_length = 80, db_index = True )
    cLocation       = models.CharField( 'location',
                        max_length = 48 )
    cCountry        = CountryField( "country" )
    cMarket         = models.CharField( 'market Global ID',
                        max_length = 14 )
    iMarket         = models.ForeignKey( Market,
                        verbose_name = 'ebay site ID', db_index=True, default = 0 ) # temporary
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88 )
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
    lCurrentPrice   = models.DecimalField( 'current price (local currency)',
                        max_digits = 10, decimal_places = 2,
                        null = True )      # use DecimalField not MoneyField
    dCurrentPrice   = models.DecimalField( # form was throwing nonsense error
                        'current price (converted to USD)', # for MoneyField
                        max_digits=10, decimal_places=2,    # but not for
                        db_index = False )     # DecimalField
    iCategoryID     = models.PositiveIntegerField( 'primary category ID',
                        null = True )
    cCategory       = models.CharField( 'primary category',
                        max_length = 48 )
    iCatHeirarchy   = models.ForeignKey( CategoryHierarchy,
                        verbose_name = 'category hierarchy (primary)',
                        related_name = 'primary_category',
                        null = True, blank = True )
    i2ndCategoryID  = models.PositiveIntegerField( 'secondary category ID (optional)',
                        null = True )
    c2ndCategory    = models.CharField( 'secondary category (optional)',
                        max_length = 48, null = True, blank = True )
    i2ndCatHeirarchy= models.ForeignKey( CategoryHierarchy,
                        verbose_name = 'category hierarchy (secondary)',
                        related_name = 'secondary_category',
                        null = True, blank = True )

    # condition is optional but may become required in the future
    # https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html
    iConditionID    = models.IntegerField( 'condition ID',
                                         null = True, blank = True )
    cCondition      = models.CharField( 'condition display name',
                        max_length = 28, null = True, blank = True )

    cSellingState   = models.CharField( 'selling state',
                        max_length = 18 )
    tCreate         = models.DateTimeField(
                        'created on', auto_now_add=True, db_index = True )

    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'itemsfound'
        db_table            = verbose_name_plural

    def get_absolute_url(self):
        #
        return reverse(
                'searching:item_found_detail',
                kwargs = { 'pk': self.pk } )



class UserItemFound(models.Model):
    iItemFound      = models.ForeignKey( ItemFound )
    dhitstars       = models.DecimalField(
                        'hit stars', max_digits = 3, decimal_places = 2,
                        null = True )
    bitemhit        = models.BooleanField( 'item of interest?',
                        default = False )    
    tlook4hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    iSearch         = models.ForeignKey( Search,
                        verbose_name = 'Search that first found this item' )
    iModel          = models.ForeignKey( Model,     null = True )
    iBrand          = models.ForeignKey( Brand,     null = True )
    iCategory       = models.ForeignKey( Category,  null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField(
                        'created on', auto_now_add=True, db_index = True )
    tModify         = models.DateTimeField(
                        'retrieved info date/time', auto_now = True )

    def __str__(self):
        return '%s - %s' % ( iUser.username, self.iItemNumb )

    class Meta:
        verbose_name_plural = 'useritemsfound'
        db_table            = verbose_name_plural
        unique_together     = ('iItemFound', 'iUser',)


'''
mistake! this is info obtained by looing up the listing, not from the finding API!
class FoundItem(models.Model):
    iItemNumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )                # itemId
    cTitle          = models.CharField(
                        'auction headline', max_length = 48, db_index = True )  # title
    mLastBid        = MoneyField( 'winning bid',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    clastbid        = models.CharField(
                        'winning bid (text)', max_length = 18,
                        db_index = False, null = True )
    tGotLastBid     = models.DateTimeField(
                        'retrieved last bid date/time', null = True )
    mBuyItNow       = MoneyField( 'buy it now price',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    cbuyitnow       = models.CharField(
                        'buy it now price (text)', max_length = 18,
                        db_index = False, null = True )
    binvaliditem    = models.BooleanField( 'invalid item?', default = False )
    iBidCount       = models.PositiveSmallIntegerField( 'number of bids' )
    tAuctionEnd     = models.DateTimeField( 'auction ending date/time' )        # startTime
    tAuctionBeg     = models.DateTimeField( 'auction beginning date/time' )
    iQuantity       = models.PositiveSmallIntegerField( 'quantity' )
    tcannotfind     = models.DateTimeField( 'cannot retrieve outcome date/time' )
    tlook4images    = models.DateTimeField(
                        'tried to retrieve images date/time', null = True )
    bgotimages      = models.NullBooleanField( 'got images?' )
    bReserveMet     = models.NullBooleanField( 'reserve met?', null = True )
    bBuyItNow       = models.BooleanField( 'buy it now?', default = False )
    bRelisted       = models.BooleanField( 'relisted?', default = False )
    cLocation       = models.CharField( 'location', max_length = 48 )           # location
    cregion         = models.CharField( 'region', max_length = 48 )
    cSeller         = models.CharField( 'seller', max_length = 48 )
    iSellerFeedback = models.PositiveIntegerField( 'seller feedback' )
    cBuyer          = models.CharField( 'buyer', max_length = 48, null = True )
    iBuyer          = models.PositiveIntegerField( 'buyer ID', null = True )
    iBuyerFeedback  = models.PositiveIntegerField(
                        'buyer feedback', null = True )
    cshipping       = models.CharField( 'shipping info', max_length = 188 )
    cDescription    = models.TextField( 'description' )
    iImages         = models.PositiveSmallIntegerField( '# of pictures' )
    iRelistItemNumb = models.BigIntegerField( 'relist item number' )
    # igetbecause   = models.ForeignKey( FetchPriorty )
    tlastcheck      = models.DateTimeField( 'got status most recently date/time' )
    bKeeper         = models.NullBooleanField( 'keep this?' )
    bNotWanted      = models.BooleanField( 'not wanted', default = False )
    bGetDetails     = models.BooleanField( 'get details', default = False )
    basktoget       = models.BooleanField( 'ask whether to get details', default = False )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'founditems'
        db_table            = verbose_name_plural
#

ebay currencies
https://developer.ebay.com/devzone/finding/callref/Enums/currencyIdList.html
AUD Australian Dollar. For eBay, you can only specify this currency for listings you submit to the Australia site (global ID EBAY-AU, site ID 15).
CAD Canadian Dollar. For eBay, you can only specify this currency for listings you submit to the Canada site (global ID EBAY-ENCA, site ID 2) (Items listed on the Canada site can also specify USD.)
CHF Swiss Franc. For eBay, you can only specify this currency for listings you submit to the Switzerland site (global ID EBAY-CH, site ID 193).
CNY Chinese Chinese Renminbi.
EUR Euro. For eBay, you can only specify this currency for listings you submit to these sites: Austria (global ID EBAY-AT, site 16), Belgium_French (global ID EBAY-FRBE, site 23), France (global ID EBAY-FR, site 71), Germany (global ID EBAY-DE, site 77), Italy (global ID EBAY-IT, site 101), Belgium_Dutch (global ID EBAY-NLBE, site 123), Netherlands (global ID EBAY-NL, site 146), Spain (global ID EBAY-ES, site 186), Ireland (global ID EBAY-IE, site 205).
GBP Pound Sterling. For eBay, you can only specify this currency for listings you submit to the UK site (global ID EBAY-GB, site ID 3).
HKD Hong Kong Dollar. For eBay, you can only specify this currency for listings you submit to the Hong Kong site (global ID EBAY-HK, site ID 201).
INR Indian Rupee. For eBay, you can only specify this currency for listings you submit to the India site (global ID EBAY-IN, site ID 203).
MYR Malaysian Ringgit. For eBay, you can only specify this currency for listings you submit to the Malaysia site (global ID EBAY-MY, site ID 207).
PHP Philippines Peso. For eBay, you can only specify this currency for listings you submit to the Philippines site (global ID EBAY-PH, site ID 211).
PLN Poland, Zloty. For eBay, you can only specify this currency for listings you submit to the Poland site (global ID EBAY-PL, site ID 212).
SEK Swedish Krona. For eBay, you can only specify this currency for listings you submit to the Sweden site (global ID EBAY-SE, site 218).
SGD Singapore Dollar. For eBay, you can only specify this currency for listings you submit to the Singapore site (global ID EBAY-SG, site 216).
TWD New Taiwan Dollar. Note that there is no longer an eBay Taiwan site.
USD US Dollar. For eBay, you can only specify this currency for listings you submit to the US (site ID 0), eBayMotors (site 100), and Canada (site 2) sites.
'''
