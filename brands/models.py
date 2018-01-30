from django.db                  import models
from django_countries.fields    import CountryField
from django.core.exceptions     import FieldDoesNotExist
from django.core.urlresolvers   import reverse

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

from regex_field.fields         import RegexField

from core.models                import IntegerRangeField



class Brand(models.Model):
    cTitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True,
        help_text = 'while searching auction titles, '
                    'bot will ignore anything in parentheses ()' )
    bWanted         = models.BooleanField(
                        'want anything from this brand?', default = True,
        help_text = 'Bot will only download full descriptions and pictures '
                    'if you want' )
    bAllOfInterest  = models.BooleanField(
                        'want everything from this brand?', default = True,
        help_text = 'Definitely set to True for desireable & rare brands' )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = 'Put common misspellings and alternate names here -- '
                    'leave blank if bot only needs to look for the brand '
                    'name. Each line evaluated separately, Bot will know '
                    'item is of this brand if any one line matches.' )
    iStars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    cComment        = models.TextField( 'comments', null = True, blank = True)
    cNationality    = CountryField( "nationality", null = True,
                        blank_label='(select country)' )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = 'Bot will know item is <b>NOT</b> of this brand if '
                    'any one line matches (each line evaluated separately, '
                    'put different exclude tests on different lines)' )
    
    oRegExLook4Title= RegexField( max_length=128, null = True )
    oRegExExclude   = RegexField( max_length=128, null = True )
    
    iLegacyKey      = models.PositiveIntegerField('legacy key', null = True )
    tLegacyCreate   = models.DateTimeField( 'legacy row created on',
                        null=True, blank = True )
    tLegacyModify   = models.DateTimeField( 'legacy row updated on',
                        null=True, blank = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                        on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )
    #

    def __str__(self):
        return self.cTitle
    
    class Meta():
        verbose_name        = 'brand name'
        verbose_name_plural = 'brands'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural

    def getCategoriesForBrand( self, oBrand ):
        #
        from categories.models  import Category
        from categories.models  import BrandCategory
        #
        oBrandCategories = BrandCategory.objects.filter( iBrand = oBrand )
        #
        oCategories = Category.objects.filter(
            id__in = BrandCategory.objects.values_list("iCategory").filter(
                iBrand = oBrand ) ).order_by( 'cTitle' )
        #
        return oCategories

    def getModelsForBrand( self, oBrand ):
        #
        from models.models import Model
        #
        oModels = Model.objects.filter( iBrand = oBrand ).order_by( 'cTitle' )
        #
        l = [ ( oModel, oModel.iCategory ) for oModel in oModels ]
        #
        return l


    def get_absolute_url(self):
        return reverse('brands:detail',
            kwargs={'pk': self.pk})
    
