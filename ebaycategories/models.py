from django.db import models

from markets.models import Market

# Create your models here.


'''
ebay_id,
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

class EbayCategory(models.Model):
    ebay_id         = models.BigIntegerField( 'ebay category number' )
    cTitle          = models.CharField(
                        'ebay category description', max_length = 48 )
    iLevel          = models.PositiveSmallIntegerField(
                        'level, top is 0, lower levels are bigger numbers' )
    iParent_ID      = models.ForeignKey( 'self',
                        verbose_name = 'parent category', related_name = 'parentcategory' )
    bLeafCategory  = models.BooleanField( 'leaf category?' )
    iTreeVersion    = models.PositiveSmallIntegerField(
                        'category tree version' )
    iMarket         = models.ForeignKey( Market, verbose_name = 'ebay market' )
    iSupercededBy   = models.ForeignKey(
                        'self', verbose_name = 'superceded by this category',
                        null = True, related_name = 'supercededby')

    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name_plural = 'ebay categories'
        db_table            = verbose_name_plural
#

class Condition(models.Model):
    ebay_id         = models.PositiveSmallIntegerField( 'ebay condition ID' )
    cTitle          = models.CharField(
                        'ebay condition description', max_length = 24 )

    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name_plural = 'ebay condition descriptions'
        db_table            = 'conditions'
    