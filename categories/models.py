from django.db                  import models

from django.contrib.auth import get_user_model
User = get_user_model()

from regex_field.fields         import RegexField

from core.models                import IntegerRangeField
from core.utils                 import getReverseWithQueryUTC

from brands.models              import Brand


class Category(models.Model):
    cTitle          = models.CharField(
                        'category description',
                        max_length = 48, db_index = True,
        help_text = 'while searching auction titles, '
                    'note: bot will ignore anything in parentheses ()' )
    cKeyWords       = models.TextField( 'category key words (optional)',
                        null = True, blank = True,
        help_text = 'Words that must be found in the title '
                    '<b>IN ADDITION TO</b> category name.  '
                    'Put alternate key words on separate lines -- '
                    'Bot will know item is for in this category if words '
                    'on any one line match.' )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = 'Put common misspellings and alternate names here -- '
                    'leave blank if bot only needs to look for the category '
                    'name. Each line evaluated separately, Bot will know '
                    'item is in this category if any one line matches.' )
    iStars          = IntegerRangeField(
                        'desireability, 10 star category is most desireable',
                            min_value = 0, max_value = 10, default = 5 )
    bAllOfInterest  = models.BooleanField(
                        'want everything of this category?', default = False,
        help_text = 'Definitely set to True for desireable & rare categories'  )
    bWantPair       = models.BooleanField('prefer pairs?', default = False,
        help_text = 'are you hoping to find these in paris?' )
    bAccessory      = models.BooleanField('accessory?', default = False)
    bComponent      = models.BooleanField('component?', default = False)
    iFamily         = models.ForeignKey( 'self',
                        verbose_name = 'category family',
                        null = True, blank = True,
        help_text = 'you can group some categories into families, '
                    'choose a category to be the lead' )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null = True, blank = True,
        help_text = 'Bot will know item is <b>NOT</b> in this category if '
                    'any one line matches (each line evaluated separately, '
                    'put different exclude tests on different lines)' )
    iLegacyKey      = models.PositiveIntegerField( 'legacy key', null=True )
    iLegacyFamily   = models.PositiveIntegerField( 'legacy family',
                                                    null = True )
    bModelsShared   = models.BooleanField(  'brands share model numbers',
                                                    default = False,
        help_text = 'Set to True if different brands use the same model '
                    'names or numbers in this category' )

    oRegExLook4Title= RegexField( max_length=128, null = True )
    oRegExKeyWords  = RegexField( max_length=128, null = True )
    oRegExExclude   = RegexField( max_length=128, null = True )
    
    tLegacyCreate   = models.DateTimeField( 'legacy row created on',
                                                    null = True )
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
        #
        return getReverseWithQueryUTC( 'categories:detail',
                    kwargs = { 'pk': self.pk } )
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
