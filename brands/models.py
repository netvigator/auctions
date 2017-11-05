from django.db                  import models
from django_countries.fields    import CountryField

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()


class IntegerRangeField(models.PositiveSmallIntegerField):
    def __init__(self,
            verbose_name=None, name=None, min_value=None, max_value=None,
            **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.PositiveSmallIntegerField.__init__(
            self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)



class Brand(models.Model):
    ctitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True)
    bwanted         = models.BooleanField(
                        'want anything from this brand?', default = True )
    ballofinterest  = models.BooleanField(
                        'want everything from this brand?', default = True )
    istars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10 )
    ccomment        = models.TextField( 'comments', null = True )
    cnationality    = CountryField( null = True )
    cexcludeif      = models.TextField(
                        'exclude item when this text is found' )
    ilegacykey      = models.PositiveIntegerField('legacy key', unique=True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on', null=True )
    iuser           = models.ForeignKey( User )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    #
    def __str__(self):
        return self.ctitle
    
    class Meta:
        verbose_name_plural = 'brands'
        ordering            = ('ctitle',)
        db_table            = verbose_name_plural
