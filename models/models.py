from django.db import models

from core.models import IntegerRangeField

from brands.models import Brand
from categories.models import Category

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Model(models.Model):
    ctitle          = models.CharField(
                        'model number or name', max_length = 48, db_index = True)
    ckeywords       = models.CharField( 'model key words', max_length = 88 )
    bkeywordrequired= models.BooleanField(
                        'key word required?', default = True )
    bsplitdigitsok  = models.BooleanField(
                        'split digits OK?', default = False )
    istars          = IntegerRangeField(
                        'desireability, 10 star model is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    bgenericmodel   = models.BooleanField('generic model?', default = True )
    bsubmodelsok    = models.BooleanField(
                        'include sub models (suffix such as A, B, C, etc.)?',
                        default = True )
    bmusthavebrand  = models.BooleanField(
                        'must have brand in aution title?', default = False)
    bwanted         = models.BooleanField('want this model?', default = True )
    bgetpictures    = models.BooleanField(
                        'want to download pics?', default = True )
    bgetdescription = models.BooleanField(
                        'want the description text?', default = True )
    ccomment        = models.TextField( 'comments', null = True, blank = True )
    ibrand          = models.ForeignKey( Brand, verbose_name = 'Brand',
                                        null = True, blank = True )
    icategory       = models.ForeignKey( Category, verbose_name = 'Category' )
    
    # maybe change to FilePathField later, it is not working now 2017-12-03
    # models.FilePathField()
    cfile1spec      = models.CharField( 'file path & name for model picture 1',
                        max_length = 48, null = True, blank = True )
    cfile2spec      = models.CharField( 'file path & name for model picture 2',
                        max_length = 48, null = True, blank = True )
    cfile3spec      = models.CharField( 'file path & name for model picture 3',
                        max_length = 48, null = True, blank = True )
    cfile4spec      = models.CharField( 'file path & name for model picture 4',
                        max_length = 48, null = True, blank = True )
    cfile5spec      = models.CharField( 'file path & name for model picture 5',
                        max_length = 48, null = True, blank = True )
    
    cexcludeif      = models.TextField(
                        'Not a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different exclude tests on different lines)',
                        null = True, blank = True )
    
    ilegacykey      = models.PositiveIntegerField('legacy key', unique=True )
    tlegacycreate   = models.DateTimeField( 'legacy row created on' )
    tlegacymodify   = models.DateTimeField( 'legacy row updated on',
                        null = True, blank = True )
    iuser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tcreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tmodify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.ctitle
        
    class Meta:
        verbose_name_plural = 'models'
        ordering            = ('ctitle',)
        db_table            = verbose_name_plural
#
