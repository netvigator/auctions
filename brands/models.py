from django.db                  import models
from django_countries.fields    import CountryField
from django.core.exceptions     import FieldDoesNotExist
from django.utils               import timezone

# Create your models here.

from django.contrib.auth        import get_user_model

from core.models                import ( IntegerRangeField, sTitleHelpText,
                                         sLookForHelpText, sExcludeIfHelpText,
                                         sLookForHeading, sKeyWordsHelpText )

from core.mixins                import GetItemsForSomething

from core.utils                 import getReverseWithUpdatedQuery

User = get_user_model()

# ### models can be FAT but not too FAT! ###


_sExplainMore = (
        '%%s<br/>Bot expands spaces and hyphens,<br/>'
        '"Hewlett-Packard" will %s Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>'
        '"Hewlett Packard" will %s Hewlett Packard, Hewlett-Packard and HewlettPackard' )

_sExplainMoreFinding = _sExplainMore % ( 'find', 'find' )

_sExplainMoreExclude = _sExplainMore % ( 'exclude', 'exclude' )


_sHelpTextBrandTitle = (
        _sExplainMoreFinding %
        ( sTitleHelpText % ( 'brand', '' ) ) )

sExample = "For example, if the brand is Chevrolet, put 'Chevy' here<br>"

_sHelpTextBrandLookFor = (
        _sExplainMoreFinding %
        ( sLookForHelpText %
            ( 'brand', 'brand', sExample, 'brand' ) ) )

_sHelpTextBrandExcludeIf = (
        _sExplainMoreExclude %
        ( sExcludeIfHelpText % 'brand' ) )


class Brand( GetItemsForSomething, models.Model ):
    cTitle          = models.CharField(
                        'brand name', max_length = 48, db_index = True,
        help_text   = _sHelpTextBrandTitle )
    bWanted         = models.BooleanField(
                        'want anything from this brand?', default = True,
        help_text = 'Bot will only download full descriptions and pictures '
                    'if you want' )
    bAllOfInterest  = models.BooleanField(
                        'want everything from this brand?', default = True,
        help_text = 'Definitely set to True for desireable & rare brands' )
    cLookFor        = models.TextField( sLookForHeading,
                        null=True, blank = True,
        help_text   = _sHelpTextBrandLookFor )
    cKeyWords       = models.TextField(
                        'brand key words',
                        null = True, blank = True,
        help_text = sKeyWordsHelpText % (
                        '', 'brand', 'brand' ) )
    iStars          = IntegerRangeField(
                        'desireability, 10 star brand is most desireable',
                        min_value = 0, max_value = 10, default = 5 )
    cComment        = models.TextField( 'comments', null = True, blank = True)
    cNationality    = CountryField( "nationality",  null = True, blank = True,
                        blank_label='(select country)' )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text   = _sHelpTextBrandExcludeIf )

    cRegExLook4Title= models.TextField( null = True )
    cRegExExclude   = models.TextField( null = True )
    cRegExKeyWords  = models.TextField( null = True )

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
        l = [ ( oModel, oModel.iStars, oModel.iCategory )
              for oModel in oModels ]
        #
        return l


    def getKeeperQsetForThis( self, oBrand, oUser ):
        #
        from keepers.models import UserKeeper
        #
        qsUserItems = (
            UserKeeper.objects.filter(
                iUser  = oUser,
                iBrand = oBrand ) )
        #
        return qsUserItems



    def getFinderQsetForThis( self, oBrand, oUser ):
        #
        from finders.models import UserItemFound
        #
        # ugh!
        # solution: denormalize, also keep tTimeEnd in UserItemFound
        #
        # qsUserItems = (
        #     UserItemFound.objects.filter(
        #         iUser  = oUser,
        #         iBrand = oBrand ).filter(
        #         iItemNumb__in = (
        #             ItemFound.objects.filter(
        #                 tTimeEnd__gt = timezone.now()
        #                 ).values_list( 'iItemNumb', flat=True ) ) ) )
        #
        qsUserItems = (
            UserItemFound.objects.filter(
                iUser               = oUser,
                iBrand              = oBrand,
                tRetrieved__isnull  = True )
            ).order_by( '-iHitStars', '-tTimeEnd' )
        #
        return qsUserItems


    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'brands:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )

