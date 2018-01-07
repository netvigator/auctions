from django.db                  import models
from django.core.urlresolvers   import reverse

from core.models                import IntegerRangeField

from brands.models              import Brand
from categories.models          import Category

from django.contrib.auth        import get_user_model
User = get_user_model()

# Create your models here.

class Model(models.Model):
    cTitle          = models.CharField(
                        'model number or name', max_length = 48,
                                        db_index = True)
    cKeyWords       = models.CharField( 'model key words', max_length = 88,
                                        null = True, blank = True )
    bKeyWordRequired= models.BooleanField(
                        'key word required?', default = True )
    bsplitdigitsok  = models.BooleanField(
                        'split digits OK?', default = False )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different look for tests on different lines)',
                        null=True, blank = True )
    iStars          = IntegerRangeField(
                        'desireability, 10 star model is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    bGenericModel   = models.BooleanField('generic model?', default = True )
    bSubModelsOK    = models.BooleanField(
                        'include sub models (suffix such as A, B, C, etc.)?',
                        default = True )
    bMustHaveBrand  = models.BooleanField(
                        'must have brand in aution title?', default = False)
    bWanted         = models.BooleanField('want this model?', default = True )
    bGetPictures    = models.BooleanField(
                        'want to download pics?', default = True )
    bGetDescription = models.BooleanField(
                        'want the description text?', default = True )
    cComment        = models.TextField( 'comments', null = True, blank = True )
    iBrand          = models.ForeignKey( Brand, verbose_name = 'Brand',
                                        null = True, blank = True )
    iCategory       = models.ForeignKey( Category, verbose_name = 'Category' )
    
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found '
                        '(each line evaluated separately, '
                        'put different exclude tests on different lines)',
                        null = True, blank = True )
    
    # maybe change to FilePathField later, it is not working now 2017-12-03
    # models.FilePathField()
    cFileSpec1      = models.CharField( 'file path & name for model picture 1',
                        max_length = 48, null = True, blank = True )
    cFileSpec2      = models.CharField( 'file path & name for model picture 2',
                        max_length = 48, null = True, blank = True )
    cFileSpec3      = models.CharField( 'file path & name for model picture 3',
                        max_length = 48, null = True, blank = True )
    cFileSpec4      = models.CharField( 'file path & name for model picture 4',
                        max_length = 48, null = True, blank = True )
    cFileSpec5      = models.CharField( 'file path & name for model picture 5',
                        max_length = 48, null = True, blank = True )
    
    iLegacyKey      = models.PositiveIntegerField('legacy key', unique=True )
    tLegacyCreate   = models.DateTimeField( 'legacy row created on' )
    tLegacyModify   = models.DateTimeField( 'legacy row updated on',
                        null = True, blank = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                        on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )
    
    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'models'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural

    def get_absolute_url(self):
        return reverse('models:detail',
            kwargs={'pk': self.pk})
#
