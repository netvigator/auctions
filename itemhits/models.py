from django.db              import models
from djmoney.models.fields  import MoneyField
from django_countries.fields \
                            import CountryField

# Create your models here.

from models.models          import Model
from brands.models          import Brand
from categories.models      import Category

from django.contrib.auth import get_user_model
User = get_user_model()

class ItemHit(models.Model):
    iItemNumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    cTitle          = models.CharField(
                        'auction headline', max_length = 48, db_index = True )
    cLocation       = models.CharField( 'location',
                        max_length = 48, null = True )
    cCountry        = CountryField( "country", null = True )
    cMarket         = models.CharField( 'market Global ID',
                        max_length = 14, null = True )
    cGalleryURL     = models.CharField( 'gallery pic URL',
                        max_length = 88, null = True )
    cEbayItemURL    = models.CharField( 'ebay item URL',
                        max_length =188, null = True )
    tTimeBeg        = models.DateTimeField( 'beginning date/time',null = True )
    tTimeEnd        = models.DateTimeField( 'ending date/time',   null = True )
    bBestOfferable  = models.BooleanField( 'best offer enabled?', default = False )
    bBuyItNowable   = models.BooleanField( 'buy it now enabled?', default = False )
    mCurrentPrice   = MoneyField( 'current price (local currency)',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    nCurrentPrice   = models.DecimalField(
                        'current price (converted to USD)',
                        max_digits=10, decimal_places=2,
                        db_index = False, null = True )
    iCategoryID     = models.IntegerField( 'primary category ID', null = True )
    cCategory       = models.CharField( 'primary category',
                        max_length = 48, null = True )
    
    iConditionID    = models.IntegerField( 'condition ID', null = True )
    cCondition      = models.CharField( 'condition display name',
                        max_length = 28, null = True )
    
    cSellingState   = models.CharField( 'selling state',
                        max_length = 18, null = True )
    
    iBidCount       = models.PositiveSmallIntegerField( 'number of bids',
                        default = 0 )
    
    dhitstars       = models.DecimalField(
                        'hit stars', max_digits = 3, decimal_places = 2 )
    bitemhit        = models.BooleanField( 'item of interest?', default = False )
    
    tlook4hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    iModel          = models.ForeignKey( Model,     null = True )
    iBrand          = models.ForeignKey( Brand,     null = True )
    iCategory       = models.ForeignKey( Category,  null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField(
                        'retrieved info date/time', auto_now = True )
    
    def __str__(self):
        return self.cTitle
        
    class Meta:
        verbose_name_plural = 'itemhits'
        db_table            = verbose_name_plural
#


class ItemImage(models.Model):
    iItemNumb       = models.ForeignKey( ItemHit )
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

