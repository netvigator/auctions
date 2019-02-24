from django.db                  import models

from django.contrib.auth import get_user_model
User = get_user_model()

from core.models                import ( IntegerRangeField, sTitleHelpText,
                                         sKeyWordsHelpText, sLookForHelpText,
                                         sExcludeIfHelpText )

from core.utils                 import getReverseWithUpdatedQuery

from brands.models              import Brand

# ### models can be FAT but not too FAT! ###

class Category(models.Model):
    cTitle          = models.CharField(
                        'category description',
                        max_length = 48, db_index = True,
        help_text = sTitleHelpText % 'category' )
    cKeyWords       = models.TextField(
                        'category key words',
                        null = True, blank = True,
        help_text = sKeyWordsHelpText % ( 'category', 'category' ) )
    cLookFor        = models.TextField(
                        'Considered a hit if this text is found (optional)',
                        null=True, blank = True,
        help_text = sLookForHelpText % ( 'category', 'category', 'category' ) +
                        '<br/>No need for plural words: plural forms of common words '
                        'in descriptioon or here will also be found.' )
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


    def getItemsForCategory( self, oCategory ):
        #
        from searching.models import UserItemFound
        from keepers.models   import Keeper
        #
        oUser = oCategory.iUser
        #
        qsUserItems = UserItemFound.objects.filter(
                iUser       = oUser,
                iCategory   = oCategory
                    ).values_list( 'iItemNumb_id', flat=True )
        #
        oItems = Keeper.objects.filter(
                iItemNumb__in = qsUserItems ).order_by( '-tTimeEnd' )[ : 20 ]
        #
        return oItems


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
