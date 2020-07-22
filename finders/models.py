from django.db          import models
from django.urls        import reverse
from django.utils       import timezone

from django_countries   import fields

from core.dj_import     import get_user_model
from core.models        import IntegerRangeField
from core.utils         import getReverseWithUpdatedQuery

from models.models      import Model
from brands.models      import Brand
from categories.models  import Category

from searching.models   import Search

from ebayinfo           import EBAY_SHIPPING_CHOICES
from ebayinfo.models    import CategoryHierarchy, Market, EbayCategory


User = get_user_model()


# Item IDs are unique across all eBay sites
# http://developer.ebay.com/devzone/shopping/docs/callref/getsingleitem.html

class ItemFound(models.Model):

    EBAY_SHIPPING_CHOICES = EBAY_SHIPPING_CHOICES

    iItemNumb       = models.BigIntegerField( 'item number',
                        primary_key = True )
    cTitle          = models.CharField( 'item title',     max_length = 80 )
    cSubTitle       = models.CharField( 'item sub title', max_length = 80,
                        null = True, blank = True )
    cLocation       = models.CharField( 'location',
                        max_length = 58 )
    cCountry        = fields.CountryField( "country" )
    cMarket         = models.CharField( 'market Global ID',
                        max_length = 14 )
    iEbaySiteID     = models.ForeignKey( Market, on_delete=models.CASCADE,
                        verbose_name = 'ebay site ID (PK)', db_index=True )
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
    lBuyItNowPrice  = models.DecimalField( 'buy it now price',
                        max_digits = 10, decimal_places = 2,
                        null = True, blank = True )
    dBuyItNowPrice  = models.DecimalField(
                        'buy it now price (converted to USD)',
                        max_digits=10, decimal_places=2,
                        null = True, blank = True )
    iShippingType   = models.PositiveSmallIntegerField(
                        'shipping type',
                        choices = EBAY_SHIPPING_CHOICES,
                        null = True ) # data prior to Feb 2019 d/n have
    iHandlingTime   = models.PositiveSmallIntegerField(
                        'hangling time',
                        null = True, blank = True ) # optional
    iCategoryID     = models.ForeignKey( EbayCategory,
                        on_delete=models.DO_NOTHING,
                        verbose_name = 'primary category ID',
                        related_name = 'ebay_primary_category',
                        null = True, blank = True ) # ebay sends but
                        # EbayCategory table is extremely slow
                        # CategoryHierarchy has relevant info & is much faster
                        # but need to get this ebay category ID from API
                        # to look up CategoryHierarchy
    cCategory       = models.CharField( 'primary category',
                        max_length = 48 )
    iCatHeirarchy   = models.ForeignKey( CategoryHierarchy,
                        on_delete=models.DO_NOTHING,
                        verbose_name = 'category hierarchy (primary)',
                        related_name = 'primary_category',
                        null = True, blank = True )
    i2ndCategoryID  = models.ForeignKey( EbayCategory,  # optional
                        on_delete=models.CASCADE,
                        verbose_name = 'secondary category ID (optional)',
                        related_name = 'ebay_secondary_category',
                        null = True, blank = True ) # ebay sends but
                        # EbayCategory table is extremely slow
                        # CategoryHierarchy has relevant info & is much faster
                        # but need to get this ebay category ID from API
                        # to look up CategoryHierarchy
    c2ndCategory    = models.CharField( 'secondary category (optional)',
                        max_length = 48, null = True, blank = True )
    i2ndCatHeirarchy= models.ForeignKey( CategoryHierarchy,
                        on_delete=models.DO_NOTHING,
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

    def get_absolute_url(self):
        #
        return reverse(
                'finders:detail', kwargs = { 'pk': self.pk } )

    class Meta:
        verbose_name_plural = 'itemsfound'
        db_table            = verbose_name_plural



class UserItemFound(models.Model):
    iItemNumb       = models.ForeignKey( ItemFound, on_delete=models.CASCADE )
    iHitStars       = IntegerRangeField(
                        'hit stars', null = True, db_index = True,
                        min_value = 0, max_value = 1000, default = 0 )
    bGetResult      = models.BooleanField( 'get results?',
                        default = False )
    tLook4Hits      = models.DateTimeField(
                        'assessed interest date/time', null = True )
    iSearch         = models.ForeignKey( Search,
                        on_delete=models.CASCADE,
                        verbose_name = 'Search that found this item' )
    iModel          = models.ForeignKey( Model, on_delete=models.CASCADE,
                        null = True, blank = True,
                        verbose_name = 'Model Name/Number',
                        help_text = 'You can display models for a particular '
                        'brand by changing to that brand (just below), '
                        'hit save, then edit again' )
    iBrand          = models.ForeignKey( Brand,  on_delete=models.CASCADE,
                        null = True, blank = True, verbose_name = 'Brand' )
    iCategory       = models.ForeignKey( Category,  on_delete=models.CASCADE,
                        null = True, blank = True,
                        verbose_name = 'Category' )
    cWhereCategory  = models.CharField( 'where category was found',
                        default = 'title',
                        max_length = 10 ) # title heirarchy1 heirarchy2
    bListExclude    = models.BooleanField( 'exclude from listing?',
                        default = False )
    # tGotPics      = models.DateTimeField( 'got pictures',
    #                   null = True, blank = True )
    bAuction        = models.BooleanField(
                        'Auction or Auction with Buy It Now',default = False )
    iUser           = models.ForeignKey( User, on_delete=models.CASCADE,
                        verbose_name = 'Owner')
    #
    # yes the col below repeats the col in ItemFound, the normalized place
    # but after writing the query to get the open auctions for a user, and
    # after considering that query's load if this project is a success,
    # it is clear that de-normalization is the way to go!!!
    # besides, time end is fixed when a seller puts up an item for auction
    # this is not a variable that will ever be maintained, once set, it is
    # absolutely fixed - seller's only option is to cancel and resubmit
    # 2019-08-27
    #
    tTimeEnd        = models.DateTimeField( 'ending date/time',
                        null=True, db_index = True  )
    #
    tCreate         = models.DateTimeField( 'created on',
                        default=timezone.now, db_index = True )
    tModify         = models.DateTimeField( 'updated on', auto_now = True )
    tRetrieved      = models.DateTimeField( 'retrieved info',
                        null = True, blank = True )
    tRetrieveFinal  = models.DateTimeField( 'retrieved info after end',
                        null = True, blank = True )
    tPutInKeepers  = models.DateTimeField( 'User has Keeper row',
                        null = True, blank = True )

    def __str__(self):
        return self.iItemNumb.cTitle

    class Meta:
        verbose_name_plural = 'useritemsfound'
        db_table            = verbose_name_plural
        unique_together     = (
                'iItemNumb', 'iUser', 'iModel', 'iBrand', 'iCategory' )

    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'finders:hit',
                kwargs = { 'pk': self.pk, 'tModify': timezone.now() } )

    def get_edit_url(self):
        #
        return reverse(
                'finders:edit', kwargs = { 'pk': self.pk } )


class UserFinder(models.Model):
    #
    # not normalized but this allows fast selection of finders for a user
    # one row per item
    # this table can now drive the finder listing for a user all by itself
    #
    iItemNumb       = models.ForeignKey( ItemFound, on_delete=models.CASCADE,
                        verbose_name = 'eBay Item Number' )
    iHitStars       = IntegerRangeField(
                        'hit stars (max for item)', null = True,
                        min_value = 0, max_value = 1000, default = 0 )
    cTitle          = models.CharField( 'item title',
                                         max_length = 80, null=True )
    cMarket         = models.CharField( 'market Global ID',
                                         max_length = 14, null=True )
    cListingType    = models.CharField( 'listing type',
                                         max_length = 15, null=True )
    tTimeEnd        = models.DateTimeField( 'ending date/time', null=True )
    iUser           = models.ForeignKey( User, on_delete=models.CASCADE,
                        verbose_name = 'Owner' )
    bGetResult      = models.NullBooleanField( 'get results?',
                        null = True, default = False )
    bListExclude    = models.NullBooleanField( 'exclude from listing?',
                        null = True, default = False )
    iMaxModel       = models.IntegerField( 'model hit with most stars',
                        null = True, default = False )
    cLookFor        = models.TextField( 'dummy for search compatibility',
                        null=True, blank = True )
    #
    def __str__(self):
        # return '%s - %s' % ( self.iItemNumb, self.iUser )
        return self.cTitle

    class Meta:
        verbose_name_plural = 'userfinders'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'iUser' )

    def get_absolute_url(self):
        #
        return reverse(
                'finders:detail', kwargs = { 'pk': self.pk } )




'''
truncate table userfinders ;

insert into userfinders ( "iItemNumb_id", "iUser_id" )
    select distinct "iItemNumb_id", "iUser_id" from useritemsfound uif
    where exists
    ( select 1 from itemsfound if
      where
        if."iItemNumb"  = uif."iItemNumb_id" and
        if."tRetrieved" is null ) ;

update userfinders uf
  set "iHitStars" =
  ( select max( uif."iHitStars" )
    from useritemsfound uif
    where
        uif."iItemNumb_id" = uf."iItemNumb_id" and
        uif."iUser_id" = uf."iUser_id" ) ;

delete from userfinders where "iHitStars" = 0 ;

update userfinders uf
  set "iMaxModel" =
  ( select distinct on (uif."iHitStars") uif."iModel_id"
    from useritemsfound uif
    where
        uif."iItemNumb_id" = uf."iItemNumb_id" and
        uif."iUser_id" = uf."iUser_id" and
        uif."iHitStars" = uf."iHitStars" ) ;

update userfinders uf
  set "bGetResult" = true where exists
  ( select 1 from useritemsfound uif
    where
      uif."iItemNumb_id" = uf."iItemNumb_id" and
      uif."iUser_id"    = uf."iUser_id" and
      uif."bGetResult" = true ) ;

temporary 2019-12-26
update useritemsfound uif
  set "bGetResult" = true where exists
  ( select 1 from userfinders uf
    where
      uf."iItemNumb_id" = uif."iItemNumb_id" and
      uf."iUser_id"     = uif."iUser_id" and
      uf."bGetResult" = true ) ;

update userfinders uf
  set "bListExclude" = false ;

update userfinders uf
  set "bListExclude" = true where exists
  ( select 1 from useritemsfound uif
    where
      uif."iItemNumb_id" = uf."iItemNumb_id" and
      uif."iUser_id" = uf."iUser_id" and
      uif."bListExclude" = true ) ;

temporary 2019-12-26:
update useritemsfound uif
  set "bListExclude" = true where exists
  ( select 1 from userfinders uf
    where
      uf."iItemNumb_id" = uif."iItemNumb_id" and
      uf."iUser_id"     = uif."iUser_id" and
      uf."bListExclude" = true ) ;

update userfinders uf
  set "cTitle"       = if."cTitle",
      "cMarket"      = if."cMarket",
      "cListingType" = if."cListingType",
      "tTimeEnd"     = if."tTimeEnd"
from itemsfound if
  where if."iItemNumb" = uf."iItemNumb_id" ;

double chek for strays:
select count(*) from userfinders where "tTimeEnd" = null ;


'''

class ItemFoundTemp(models.Model):
    iItemNumb       = models.ForeignKey( ItemFound, on_delete=models.CASCADE )
    iHitStars       = IntegerRangeField(
                        'hit stars', null = True,
                        min_value = 0, max_value = 1000, default = 0 )
    iSearch         = models.ForeignKey( Search,  on_delete=models.CASCADE,
                        verbose_name = 'Search that first found this item' )
    iModel          = models.ForeignKey( Model, on_delete=models.CASCADE,
                        null = True )
    iBrand          = models.ForeignKey( Brand, on_delete=models.CASCADE,
                        null = True )
    iCategory       = models.ForeignKey( Category, on_delete=models.CASCADE,
                        null = True )
    iStarsModel     = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )
    iStarsBrand     = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )
    iStarsCategory  = IntegerRangeField( null = True,
                        min_value = 0, max_value = 10, default = 1 )
    cFoundModel     = models.CharField(
                        'model name/number found in auction title',
                        max_length = 48,            null = True )
    iFoundModelLen  = models.PositiveSmallIntegerField( default = 0 )
    bModelKeyWords  = models.NullBooleanField(
                        'model has key words and they are in auction title?',
                        null = True, default = False )
    cModelAlphaNum  = models.CharField(
                        'model name/number alpha num only',
                        max_length = 48,            null = True )
    cTitleLeftOver  = models.CharField( 'item title less model match',
                        max_length = 80,            null = True )
    cWhereCategory  = models.CharField( 'where category was found',
                        default = 'title',
                        max_length = 10 ) # title heirarchy1 heirarchy2
    bIncludeThis    = models.BooleanField(
                        'include this hit when populating table?',
                        default = True )

    def __str__(self):
        #
        lOut = [ 'ItemFound - %s' % self.iItemNumb ]
        #
        for s in vars( self ):
            if s.startswith( '_' ): continue
            lOut.append( '    %s: %s' % ( s, self.__dict__[s] ) )
        #
        return '\n'.join( lOut )

    class Meta:
        verbose_name_plural = 'itemsfoundtemp'
        db_table            = verbose_name_plural


