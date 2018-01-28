from django.db                  import models
from django.core.urlresolvers   import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from regex_field.fields         import RegexField

from core.models                import IntegerRangeField

from brands.models              import Brand


class Category(models.Model):
    cTitle          = models.CharField(
                        'category description',
                        max_length = 48, db_index = True,
        help_text = 'while searching auction titles, '
                    'bot will ignore anything in parentheses ()' )
    cKeyWords       = models.CharField( 'category key words', max_length = 88,
                                        null = True, blank = True,
        help_text = 'Bot will look for this text in the item description -- '
                    'use the vertical bar "|" between alternate key words' )
    bKeyWordRequired= models.BooleanField(
                        'key word required?', default = False,
        help_text = 'Bot will know this model is for sale only '
                    'if these key words are in the description' )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found',
                        null=True, blank = True,
        help_text = 'Leave blank if bot only needs to look for the category '
                    'name. Each line evaluated separately, '
                    'put different look for tests on different lines.' )
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
                        'Not a hit if this text is found',
                        null = True, blank = True,
        help_text = 'Not a hit if this text is found '
                    '(each line evaluated separately, '
                    'put different exclude tests on different lines)' )
    iLegacyKey      = models.PositiveIntegerField( 'legacy key', null=True )
    iLegacyFamily   = models.PositiveIntegerField( 'legacy family',
                                                    null = True )
    bModelsShared   = models.BooleanField(  'brands share model numbers',
                                                    default = False,
        help_text = 'Set to True if different brands use the same model '
                    'names or numbers in this category' )

    oRegExFound     = RegexField( max_length=128, null = True )
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
