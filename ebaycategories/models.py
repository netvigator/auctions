from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from markets.models import Market

# Create your models here.


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
    iMarket         = models.ForeignKey( Market, verbose_name = 'ebay market' )
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
    
    class Meta():
        verbose_name_plural = 'ebay categories'
        db_table        = verbose_name_plural
        unique_together = ('iCategoryID', 'iMarket',)

    class MPTTMeta:
        order_insertion_by = ['name']

#

class Condition(models.Model):
    iConditionID    = models.PositiveSmallIntegerField( 'ebay condition ID' )
    cTitle          = models.CharField(
                        'ebay condition description', max_length = 24 )

    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name_plural = 'ebay condition descriptions'
        db_table            = 'conditions'
    