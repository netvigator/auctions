from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

# moved class IntegerRangeField() to core.models
from core.models import IntegerRangeField

# from categories.models  import Category




class Brand(models.Model):
    ctitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True)
    bwanted         = models.BooleanField(
                        'want anything from this brand?', default = True )
    ballofinterest  = models.BooleanField(
                        'want everything from this brand?', default = True )
    istars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    ccomment        = models.TextField( 'comments', null = True, blank = True )
    cnationality    = CountryField( "nationality", null = True )
    cexcludeif      = models.TextField(
                        'Not a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different exclude tests on different lines)',
                        null=True, blank = True )
    ilegacykey      = models.PositiveIntegerField('legacy key', null = True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on',
                        null=True, blank = True )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on',
                        null=True, blank = True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    #

    def __str__(self):
        return self.ctitle
    
    class Meta():
        verbose_name_plural = 'brands'
        ordering            = ('ctitle',)
        db_table            = verbose_name_plural

