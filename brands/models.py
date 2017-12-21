from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

# moved class IntegerRangeField() to core.models
from core.models import IntegerRangeField

# from categories.models  import Category




class Brand(models.Model):
    cTitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True)
    bWanted         = models.BooleanField(
                        'want anything from this brand?', default = True )
    bAllOfInterest  = models.BooleanField(
                        'want everything from this brand?', default = True )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different look for tests on different lines)',
                        null=True, blank = True )
    iStars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    cComment        = models.TextField( 'comments', null = True, blank = True )
    cNationality    = CountryField( "nationality", null = True )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different exclude tests on different lines)',
                        null=True, blank = True )
    iLegacyKey      = models.PositiveIntegerField('legacy key', null = True )
    tLegacyCreate   = models.DateTimeField( 'legacy row created on',
                        null=True, blank = True )
    tLegacyModify   = models.DateTimeField( 'legacy row updated on',
                        null=True, blank = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )
    #

    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name_plural = 'brands'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural

