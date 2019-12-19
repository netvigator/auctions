from django.db                  import models
from django.utils               import timezone

from django.contrib.auth        import get_user_model

from core.models                import ( IntegerRangeField, sTitleHelpText,
                                         sKeyWordsHelpText, sLookForHelpText,
                                         sExcludeIfHelpText, sLookForHeading )

from core.mixins                import GetItemsForSomething

from core.utils                 import getReverseWithUpdatedQuery

from brands.models              import Brand

User = get_user_model()

# ### models can be FAT but not too FAT! ###

class Category( GetItemsForSomething, models.Model ):
    cTitle          = models.CharField(
                        'category description', # test_core_tags expects this
                        max_length = 48, db_index = True,
        help_text = sTitleHelpText % ( 'category', '<em>AND</em> category heirachy ' ) )
    cKeyWords       = models.TextField(
                        'category key words',
                        null = True, blank = True,
        help_text = sKeyWordsHelpText % ( 'category', 'category' ) )
    cLookFor        = models.TextField( sLookForHeading,
                        null=True, blank = True,
        help_text = sLookForHelpText % ( 'category', 'category', '', 'category' ) +
                        '<br/>No need for plural words: plural forms of common words '
                        'in description or here will also be found.' )
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
                        null = True, blank = True, on_delete=models.CASCADE,
        help_text = 'you can group some categories into families, '
                    'choose a category to be the lead' )
    cExcludeIf      = models.TextField(
                        'Not a hit if this text is found (optional)',
                        null = True, blank = True,
        help_text = sExcludeIfHelpText % 'category' )
    iLegacyKey      = models.PositiveIntegerField( 'legacy key', null=True )
    iLegacyFamily   = models.PositiveIntegerField( 'legacy family',
                                                    null = True )
    bModelsShared   = models.BooleanField(  'brands share model numbers',
                                                    default = False,
        help_text = 'Set to True if different brands use the same model '
                    'names or numbers in this category' )

    cRegExLook4Title= models.TextField( null = True )
    cRegExExclude   = models.TextField( null = True )
    cRegExKeyWords  = models.TextField( null = True )

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

    class Meta:
        verbose_name_plural = 'categories'
        ordering            = ('cTitle',)
        db_table            = verbose_name_plural
        unique_together     = ('cTitle','iUser')


    def getKeeperQsetForThis( self, oCategory, oUser ):
        #
        from keepers.models import UserKeeper
        #
        qsUserItems = (
            UserKeeper.objects.filter(
                iUser       = oUser,
                iCategory   = oCategory ) )
        #
        return qsUserItems



    def getFinderQsetForThis( self, oCategory, oUser ):
        #
        from finders.models import UserItemFound
        #
        # ugh!
        # solution: denormalize, also keep tTimeEnd in UserItemFound
        #
        # qsUserItems = (
        #     UserItemFound.objects.filter(
        #         iUser  = oUser,
        #         iCategory   = oCategory ).filter(
        #         iItemNumb__in = (
        #             ItemFound.objects.filter(
        #                 tTimeEnd__gt = timezone.now()
        #                 ).values_list( 'iItemNumb', flat=True ) ) ) )
        #
        qsUserItems = (
            UserItemFound.objects.filter(
                iUser        = oUser,
                iCategory    = oCategory,
                tTimeEnd__gt = timezone.now() ) )
        #
        return qsUserItems


    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'categories:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )
#


class BrandCategory(models.Model):
    iBrand          = models.ForeignKey( Brand,
                            on_delete=models.CASCADE )
    iCategory       = models.ForeignKey( Category,
                            on_delete=models.CASCADE )
    bWant           = models.BooleanField('want this combination?', default = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                            on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )

    class Meta:
        verbose_name_plural = 'brandcategories'
        db_table            = verbose_name_plural
#
