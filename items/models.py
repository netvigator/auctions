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

