from django.db import models
from django_countries.fields    import CountryField

# Create your models here.

# table of ebay MarketPlaces:
# https://developer.ebay.com/api-docs/static/rest-request-components.html#HTTP

class Market(models.Model):
    cmarket     = models.CharField( 'market',    max_length = 14 )
    ccountry    = CountryField(     'country',   null = True )
    clanguages  = models.CharField( 'languages', max_length = 28 )

    def __str__(self):
        return self.cmarket
    
    class Meta():
        verbose_name_plural = 'markets'
        ordering            = ('cmarket',)
        db_table            = verbose_name_plural

