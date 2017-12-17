from django.db.models           import PositiveSmallIntegerField as SmallInt
from django.db.models           import Model, CharField, NullBooleanField
from django_countries.fields    import CountryField

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
    cmarket         = CharField(    'ebay Global ID',    max_length = 14,
                                unique = True )
    ccountry        = CountryField( 'country' )
    clanguage       = CharField(    'language',  max_length = 8 )
    iebaysiteid     = SmallInt(     'site ID', unique=True )
    bhascategories  = NullBooleanField( 'has own categories?', null = True )
    icategoryver    = SmallInt(     'most recent category version',
                               null = True )
    ccurrencydef    = CharField(    'currency default',
                               max_length = 3, null = True )
    
    def __str__(self):
        return self.cmarket
    
    class Meta():
        verbose_name_plural = 'markets'
        ordering            = ('cmarket',)
        db_table            = verbose_name_plural

