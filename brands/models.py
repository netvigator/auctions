from django.db                  import models
from django_countries.fields    import CountryField
from django.core.exceptions     import FieldDoesNotExist

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

from core.models                import ( IntegerRangeField, sTitleHelpText,
                                         sLookForHelpText, sExcludeIfHelpText )

from core.utils                 import getReverseWithUpdatedQuery


# ### models can be FAT but not too FAT! ###


class Brand(models.Model):
    cTitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True,
        help_text = sTitleHelpText % 'brand' )
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
        help_text = sLookForHelpText % ( 'brand', 'brand', 'brand' ) )
    iStars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    cComment        = models.TextField( 'comments', null = True, blank = True)
    cNationality    = CountryField( "nationality",  null = True, blank = True,
                        blank_label='(select country)' )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = sExcludeIfHelpText % 'brand' )

    cRegExLook4Title= models.TextField( null = True )
    cRegExExclude   = models.TextField( null = True )

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

    class Meta:
        verbose_name        = 'brand name'
        verbose_name_plural = 'brands'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural
        unique_together     = ('cTitle','iUser')

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

    def getItemsForBrand( self, oBrand ):
        #
        from searching.models import UserItemFound
        from keepers.models   import Keeper
        #
        oUser = oBrand.iUser
        #
        qsUserItems = UserItemFound.objects.filter(
                iUser  = oUser,
                iBrand = oBrand ).values_list( 'iItemNumb_id', flat=True )
        #
        oItems = Keeper.objects.filter(
                iItemNumb__in = qsUserItems ).order_by( '-tTimeEnd' )[ : 20 ]
        #
        return oItems



    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'brands:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )

