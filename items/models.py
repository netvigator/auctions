from django.db import models
from djmoney.models.fields  import MoneyField

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class Item(models.Model):
    iitemnumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    ctitle          = models.CharField(
                        'auction headline', max_length = 48, db_index = True )
    mlastbid        = MoneyField( 'winning bid',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    clastbid        = models.CharField(
                        'winning bid (text)', max_length = 18,
                        db_index = False, null = True )
    tgotlastbid     = models.DateTimeField(
                        'retrieved last bid date/time', null = True )
    mbuyitnow       = MoneyField( 'buy it now price',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    cbuyitnow       = models.CharField(
                        'buy it now price (text)', max_length = 18,
                        db_index = False, null = True )
    binvaliditem    = models.BooleanField( 'invalid item?', default = False )
    inumberofbids   = models.PositiveSmallIntegerField( 'number of bids' )
    tauctionend     = models.DateTimeField( 'auction ending date/time' )
    tauctionbeg     = models.DateTimeField( 'auction beginning date/time' )
    iquantity       = models.PositiveSmallIntegerField( 'quantity' )
    tcannotfind     = models.DateTimeField( 'cannot retrieve outcome date/time' )
    tlook4images    = models.DateTimeField(
                        'tried to retrieve images date/time', null = True )
    bgotimages      = models.NullBooleanField( 'got images?' )
    breservemet     = models.NullBooleanField( 'reserve met?', null = True )
    bbuyitnow       = models.BooleanField( 'buy it now?', default = False )
    brelisted       = models.BooleanField( 'relisted?', default = False )
    clocation       = models.CharField( 'location', max_length = 48 )
    cregion         = models.CharField( 'region', max_length = 48 )
    cseller         = models.CharField( 'seller', max_length = 48 )
    isellerfeedback = models.PositiveIntegerField( 'seller feedback' )
    cbuyer          = models.CharField( 'buyer', max_length = 48, null = True )
    ibuyer          = models.PositiveIntegerField( 'buyer ID', null = True )
    ibuyerfeedback  = models.PositiveIntegerField(
                        'buyer feedback', null = True )
    cshipping       = models.CharField( 'shipping info', max_length = 188 )
    cdescription    = models.TextField( 'description' )
    iimages         = models.PositiveSmallIntegerField( '# of pictures' )
    irelistitemnumb = models.BigIntegerField( 'relist item number' )
    # igetbecause   = models.ForeignKey( FetchPriorty )
    tlastcheck      = models.DateTimeField( 'got status most recently date/time' )
    bkeeper         = models.NullBooleanField( 'keep this?' )
    bnotwanted      = models.BooleanField( 'not wanted', default = False )
    bgetdetails     = models.BooleanField( 'get details', default = False )
    basktoget       = models.BooleanField( 'ask whether to get details', default = False )
    iuser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.ctitle
        
    class Meta:
        verbose_name_plural = 'items'
        db_table            = verbose_name_plural
#

'''
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

class ItemImage(models.Model):
    iitemnumb       = models.ForeignKey( Item )
    isequence       = models.PositiveSmallIntegerField( 'sequence' )
    cfilename       = models.CharField( 'local file name', max_length = 28 )
    coriginalurl    = models.TextField( 'original URL' )
    iuser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    def __str__(self):
        return self.iitemnumb

    class Meta:
        verbose_name_plural = 'itemimages'
        db_table            = verbose_name_plural
        unique_together     = ('iitemnumb', 'isequence',)
#

