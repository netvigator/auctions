from django.db                  import models
from django.core.urlresolvers   import reverse

# Create your models here.

# moved class IntegerRangeField() to core.models
from core.models import IntegerRangeField


from django.contrib.auth import get_user_model
User = get_user_model()

from brands.models import Brand

class Category(models.Model):
    cTitle          = models.CharField(
                        'category description', max_length = 48, db_index = True)
    cKeyWords       = models.CharField( 'category key words', max_length = 88,
                                        null = True, blank = True )
    bKeyWordRequired= models.BooleanField(
                        'key word required?', default = False )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different look for tests on different lines)',
                        null=True, blank = True )
    iStars          = IntegerRangeField(
                        'desireability, 10 star category is most desireable',
                            min_value = 0, max_value = 10, default = 5 )
    bAllOfInterest  = models.BooleanField(
                        'want everything of this category?', default = False )
    bWantPair       = models.BooleanField('only want pairs?', default = False)
    bAccessory      = models.BooleanField('accessory?', default = False)
    bComponent      = models.BooleanField('component?', default = False)
    iFamily         = models.ForeignKey( 'self',
                        verbose_name = 'category family', null = True, blank = True )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different exclude tests on different lines)',
                        null = True, blank = True )
    iLegacyKey      = models.PositiveIntegerField( 'legacy key', unique=True )
    iLegacyFamily   = models.PositiveIntegerField( 'legacy family',
                                                    null = True )
    bModelsShared   = models.BooleanField(  'brands share model numbers',
                                                    default = False)
    tLegacyCreate   = models.DateTimeField( 'legacy row created on' )
    tLegacyModify   = models.DateTimeField( 'legacy row updated on',
                                            null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                        on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name_plural = 'categories'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural

    def get_absolute_url(self):
        return reverse('categories:detail',
            kwargs={'pk': self.pk})
#


class BrandCategory(models.Model):
    iBrand          = models.ForeignKey( Brand )
    iCategory       = models.ForeignKey( Category )
    bWant           = models.BooleanField('want this combination?', default = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    class Meta:
        verbose_name_plural = 'brandcategories'
        db_table            = verbose_name_plural
#
