from django.db              import models
from djmoney.models.fields  import MoneyField

# Create your models here.

from models.models          import Model
from brands.models          import Brand
from categories.models      import Category

from django.contrib.auth import get_user_model
User = get_user_model()

class ItemHit(models.Model):
    iitemnumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    ctitle          = models.CharField(
                        'auction headline', max_length = 48, db_index = True )
    mlastbid        = MoneyField( 'most recent bid',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    clastbid        = models.CharField(
                        'most recent bid (text)', max_length = 18,
                        db_index = False, null = True )
    mbuyitnow       = MoneyField( 'buy it now price',
                        max_digits = 10, decimal_places = 2,
                        default_currency='USD', null = True )
    cbuyitnow       = models.CharField(
                        'buy it now price (text)', max_length = 18,
                        db_index = False, null = True )
    inumberofbids   = models.PositiveSmallIntegerField( 'number of bids', default = 0 )
    tauctionend     = models.DateTimeField( 'auction ending date/time' )
    tauctionbeg     = models.DateTimeField( 'auction beginning date/time' )
    dhitstars       = models.DecimalField(
                        'hit stars', max_digits = 3, decimal_places = 2 )
    bitemhit        = models.BooleanField( 'item of interest?', default = False )
    tlook4hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    imodel          = models.ForeignKey( Model,     null = True )
    ibrand          = models.ForeignKey( Brand,     null = True )
    icategory       = models.ForeignKey( Category,  null = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField(
                        'retrieved info date/time', auto_now = True )
    
    def __str__(self):
        return self.ctitle
        
    class Meta:
        verbose_name_plural = 'itemhits'
        db_table            = verbose_name_plural
#

