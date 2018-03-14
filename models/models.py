from django.db                  import models

from crispy_forms.helper        import FormHelper
from crispy_forms.layout        import Submit

from django.contrib.auth        import get_user_model
User = get_user_model()

from regex_field.fields         import RegexField

from core.models                import (
                            gotSomethingOutsideTitleParensCharField,
                            IntegerRangeField, sTitleHelpText,
                            sKeyWordsHelpText, sLookForHelpText,
                            sExcludeIfHelpText )

from core.utils                 import getReverseWithUpdatedQuery

from brands.models              import Brand
from categories.models          import Category



class Model( models.Model ):
    cTitle          = gotSomethingOutsideTitleParensCharField(
                        'model number or name',
                        max_length = 48, db_index = True,
        help_text = sTitleHelpText % 'model number or' )
    cKeyWords       = models.TextField( 'model key words (optional)',
                        null = True, blank = True,
        help_text = sKeyWordsHelpText % ( 'model number or', 'model' ) )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = sLookForHelpText % (
                            'model numbers or', 'model number or', 'model' ) )
    iStars          = IntegerRangeField(
                        'desireability, 10 star model is most desireable',
                        min_value = 0, max_value = 10, default = 5,
        help_text = 'Bot considers when deciding whether '
                    'to download full description and pictures' )
    bGenericModel   = models.BooleanField('generic model?', default = False,
        help_text = 'model name/number is used by more than one brand' )
    bSubModelsOK    = models.BooleanField(
                        'include sub models (suffix such as A, B, C, etc.)?',
                        default = True,
        help_text = 'Set to False when you want to track the submodels '
                    'separately (so you should enter a model record '
                    'for each submodel)' )
    bMustHaveBrand  = models.BooleanField(
                        'must have brand in aution title?', default = False,
        help_text = 'Bot will know item for sale is this model only if '
                    'Brand name is in the auction title (useful when model '
                    'name/number is common (example: Model T Ford; '
                    '"T" is common)' )
    bWanted         = models.BooleanField('want this model?', default = True,
        help_text = 'Bot will download full descriptions and pictures only if '
                    'you do want to track this model' )
    bGetPictures    = models.BooleanField(
                        'want to download pics?', default = True,
        help_text = 'Bot will download pictures only if you want them' )
    bGetDescription = models.BooleanField(
                        'want the description text?', default = True,
        help_text = 'Bot will download full descriptions only if '
                    'you do want them' )
    cComment        = models.TextField( 'comments', null = True, blank = True )
    iBrand          = models.ForeignKey( Brand, verbose_name = 'Brand',
                            null = True, blank = True,
                            on_delete=models.CASCADE )
    iCategory       = models.ForeignKey( Category, verbose_name = 'Category',
                            on_delete=models.CASCADE )
    
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null = True, blank = True,
        help_text = sExcludeIfHelpText % 'model' )
    
    oRegExLook4Title= RegexField( max_length=128, null = True )
    oRegExKeyWords  = RegexField( max_length=128, null = True )
    oRegExExclude   = RegexField( max_length=128, null = True )
    
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
    
    iLegacyKey      = models.PositiveIntegerField('legacy key', null=True )
    tLegacyCreate   = models.DateTimeField( 'legacy row created on',
                        null = True )
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
        #
        return getReverseWithUpdatedQuery(
                'models:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )
#
