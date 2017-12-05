from django.db import models

from markets.models import Market

# Create your models here.


'''
ebay_id,
ctitle, 
ilevel, 
iparent_id, 
bleaf_category,
iTreeVersion,
imarket,
isupercededby
'''

# http://developer.ebay.com/devzone/xml/docs/reference/ebay/getcategories.html
# category numbers are only unique within a marketplace site

class EbayCategory(models.Model):
    ebay_id         = models.BigIntegerField( 'ebay category number' )
    ctitle          = models.CharField(
                        'ebay category description', max_length = 48 )
    ilevel          = models.PositiveSmallIntegerField(
                        'level, top is 0, lower levels are bigger numbers' )
    iparent_id      = models.ForeignKey(
                        'self', verbose_name = 'parent category' )
    bleaf_category  = models.BooleanField( 'leaf category?' )
    iTreeVersion    = models.PositiveSmallIntegerField(
                        'category tree version' )
    iMarket         = models.ForeignKey( Market, verbose_name = 'ebay market' )
    isupercededby   = models.ForeignKey(
                        'self', verbose_name = 'superceded by this category',
                        null = True )

    def __str__(self):
        return self.ctitle
    
    class Meta():
        verbose_name_plural = 'ebay categories'
        db_table            = verbose_name_plural
#
