from django.db.models           import PositiveSmallIntegerField as SmallInt
from django.db.models           import Model, CharField
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

class Market(Model):
    cmarket     = CharField(    'market',    max_length = 14, unique=True )
    ccountry    = CountryField( 'country' )
    clanguage   = CharField(    'language',  max_length = 8 )
    iebaysiteid = SmallInt(     'global ID', unique=True )

    def __str__(self):
        return self.cmarket
    
    class Meta():
        verbose_name_plural = 'markets'
        ordering            = ('cmarket',)
        db_table            = verbose_name_plural

