from django.core.validators     import MaxValueValidator, MinValueValidator
from django.db                  import models
from django.db.models           import PositiveSmallIntegerField as PosSmallInt
from django.db.models           import Model, CharField, NullBooleanField
from django.db.models           import SmallIntegerField as SmallInt
from django_countries.fields    import CountryField
from mptt.models                import MPTTModel, TreeForeignKey

from core.models                import UpperCaseCharField

# Create your models here.

#### INVALID ###
# table of INVALID ebay MarketPlaces:
# https://developer.ebay.com/api-docs/static/rest-request-components.html#HTTP
# heading:
# Marketplace ID and language header values

# notes in core/ebay_wrapper.py tell which global ID to use with which call
# http://developer.ebay.com/devzone/finding/Concepts/SiteIDToGlobalID.html
# http://developer.ebay.com/DevZone/half-finding/CallRef/Enums/GlobalIdList.html

# not all markets have their own categories
# https://developer.ebay.com/api-docs/commerce/taxonomy/static/supportedmarketplaces.html
# also A given eBay marketplace might use multiple category trees
# https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getDefaultCategoryTreeId

#### NOTE Russia is on the list of markets with own category list but d/n have id for the market!
# https://developer.ebay.com/api-docs/commerce/taxonomy/static/supportedmarketplaces.html
# ebay.com/sch/Russia is website, but that is a category on USA site, forget Russia

# currencies:
# https://developer.ebay.com/devzone/finding/callref/Enums/currencyIdList.html

class Market(Model):
    iEbaySiteID     = PosSmallInt(          'site ID', primary_key = True )
    cMarket         = UpperCaseCharField(   'ebay Global ID', max_length = 14,
                                unique = True )
    cCountry        = CountryField(         'country' )
    cLanguage       = CharField(            'language',  max_length = 8 )
    bHasCategories  = NullBooleanField(     'has own categories?', null=True)
    iCategoryVer    = PosSmallInt(          'most recent category version',
                                null = True )
    cCurrencyDef    = UpperCaseCharField(   'currency default',
                                max_length = 3, null = True )
    cUseCategoryID  = UpperCaseCharField(
                                'uses category list from this Market',
                                max_length = 14, null = True, blank = True )
    iUtcPlusOrMinus = SmallInt(             'UTC offset', null=True,
                               validators=[ MaxValueValidator( 12),
                                            MinValueValidator(-12)] )

    def __str__(self):
        return self.cMarket
    
    class Meta:
        verbose_name_plural = 'markets'
        ordering            = ('cMarket',)
        db_table            = verbose_name_plural


'''
iCategoryID,
cTitle, 
iLevel, 
iParent_ID, 
bLeafCategory,
iTreeVersion,
imarket,
iSupercededBy
'''

# http://developer.ebay.com/devzone/xml/docs/reference/ebay/getcategories.html
# category numbers are only unique within a marketplace site

# if the context was postgresql only,
# category number + market ID could be the (compound) primary key
# BUT
# 1) django does not support compound primary keys, 
# and
# 2) MPTT requires parent, which refers to id

class EbayCategory(MPTTModel):
    iCategoryID     = models.PositiveIntegerField( 'ebay category number',
                        db_index=True )
    name            = models.CharField(
                        'ebay category description', max_length = 50 )
    iLevel          = models.PositiveSmallIntegerField(
                        'ebay level (top is 1, lower levels are bigger numbers)' )
    iParentID       = models.PositiveIntegerField( 'ebay parent category' )
    bLeafCategory   = models.BooleanField( 'leaf category?' )
    iTreeVersion    = models.PositiveSmallIntegerField( 
                        'category tree version' )
    #models.ForeignKey( Market, PositiveIntegerField
    iMarket         = models.ForeignKey( Market,
                        verbose_name = 'ebay market', db_index=True,
                        on_delete=models.CASCADE )
    iSupercededBy   = models.PositiveIntegerField(
                        'superceded by this ebay category', null = True )
    parent          = TreeForeignKey( 'self',
                        null=True, blank=True, related_name='children',
                        db_index=True)
    
    '''
    column required by mptt:
    parent
    
    columns added by mptt:
    level
    lft
    rght
    tree_id
    
    changing the subject:
    if there are lots of superceded categories, can do this manually via psql:
    CREATE INDEX ON "ebay categories" ("iSupercededBy") WHERE "iSupercededBy" IS NOT NULL;
    but not worth it if there are only a small percent of superceded categories
    '''

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'ebay categories'
        db_table            = 'ebay_categories'
        unique_together     = ('iCategoryID', 'iMarket',)

    class MPTTMeta:
        order_insertion_by  = ['name']



class CategoryHierarchy(models.Model):

    iCategoryID     = models.PositiveIntegerField( 'ebay category number',
                        db_index=True )
    iMarket         = models.ForeignKey( Market,
                        verbose_name = 'ebay market', db_index=True,
                        on_delete=models.CASCADE )
    cCatHierarchy   = models.TextField( 'category hierarchy',
                        null = True, blank = True)
    
    class Meta:
        verbose_name_plural = 'category hierarchies'
        db_table            = 'category_hierarchies'
        unique_together     = ('iCategoryID', 'iMarket',)
        ordering            = ('iMarket','iCategoryID')



class Condition(models.Model):
    iConditionID    = models.PositiveSmallIntegerField( 'ebay condition ID' )
    cTitle          = models.CharField(
                        'ebay condition description', max_length = 24 )

    def __str__(self):
        return self.cTitle
    
    class Meta:
        verbose_name_plural = 'ebay condition descriptions'
        db_table            = 'conditions'


