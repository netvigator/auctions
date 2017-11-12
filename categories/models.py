from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

# moved class IntegerRangeField() to core.models
from core.models import IntegerRangeField


from django.contrib.auth import get_user_model
User = get_user_model()

from brands.models import Brand

class Category(models.Model):
    ctitle          = models.CharField(
                        'category description', max_length = 48, db_index = True)
    ckeywords       = models.CharField( 'category key words', max_length = 88 )
    bkeywordrequired= models.BooleanField(
                        'key word required?', default = True )
    istars          = IntegerRangeField(
                        'desireability, 10 star category is most desireable',
                            min_value = 0, max_value = 10 )
    ballofinterest  = models.BooleanField(
                        'want everything of this category?', default = True )
    bwantpair       = models.BooleanField('only want pairs?', default = False)
    baccessory      = models.BooleanField('accessory?', default = False)
    bcomponent      = models.BooleanField('component?', default = False)
    ifamily         = models.ForeignKey( 'self', null = True )
    ilegacykey      = models.PositiveIntegerField( 'legacy key', unique=True )
    ilegacyfamily   = models.PositiveIntegerField( 'legacy family',
                                                    null = True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on',
                                            null = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.ctitle
    
    class Meta():
        verbose_name_plural = 'categories'
        ordering            = ('ctitle',)
        db_table            = verbose_name_plural
#


class BrandCategory(models.Model):
    ibrand          = models.ForeignKey( Brand )
    icategory           = models.ForeignKey( Category )
    bwanted         = models.BooleanField('want this combination?', default = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    class Meta:
        verbose_name_plural = 'brandcategories'
        db_table            = verbose_name_plural
#
