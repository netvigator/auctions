from django.db          import models

from core.utils         import getReverseWithUpdatedQuery

from ebayinfo.models    import EbayCategory

from core.dj_import     import get_user_model
User = get_user_model()

from pyPks.Time.Output  import getIsoDateTimeFromDateTime


# ### models can be FAT but not too FAT! ###



class Search(models.Model):
    cTitle          = models.CharField( 'short description',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'search for key words (maximum length 350 characters)',
        max_length = 350, null = True, blank = True,
        help_text = 'What you type here will go into the ebay serch box '
                    '-- mulitple terms will result in an AND search.  '
                    'TIPS: to exclude words, put a - in front '
                    '(without any space), '
                    'search for red OR green handbags as follows: '
                    'handbags (red,green)  search for handbags but '
                    'exclude red and green as follows: '
                    'handbags -(red,green)  350 characters MAX' )
    # max length for a single key word is 98
    #models.ForeignKey( EbayCategory, models.PositiveIntegerField(
    iEbayCategory   = models.ForeignKey( EbayCategory,
                        verbose_name = 'ebay category (optional)',
                        null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!) '
                    '(Both are OK)', on_delete=models.CASCADE )
    iDummyCategory  = models.PositiveIntegerField( 'ebay category number',
                                null = True, blank = True,
        help_text = 'Limit search to items listed in this category '
                    '-- (key words OR ebay category required!)' )
    cPriority       = models.CharField( 'processing priority',
                                max_length = 2, null = True,
                                choices = (),
        help_text = 'high priority A1 A2 A3 ... Z9 low priority' )
    tBegSearch      = models.DateTimeField( 'last search started',
                                           null = True )
    tEndSearch      = models.DateTimeField( 'last search completed',
                                           null = True )
    cLastResult     = models.TextField( 'last search outcome', null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner',
                            on_delete=models.CASCADE )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )

    def __str__(self):
        return self.cTitle

    class Meta:
        verbose_name_plural = 'searches'
        db_table        = 'searching'
        unique_together = ( ( 'iUser',      'cPriority' ),
                            ( 'iUser',      'cTitle'    ),
                            ( 'iUser',      'cKeyWords',   'iEbayCategory',) )
        ordering        = ('cTitle',)

    def get_absolute_url(self):
        #
        return getReverseWithUpdatedQuery(
                'searching:detail',
                kwargs = { 'pk': self.pk, 'tModify': self.tModify } )



class SearchLog(models.Model):
    iSearch     = models.ForeignKey( Search,
                        verbose_name = 'Search that first found this item',
                        on_delete=models.CASCADE )
    tBegSearch  = models.DateTimeField( 'search started',
                        db_index = True )
    tEndSearch  = models.DateTimeField( 'search completed',
                        null = True )
    tBegStore   = models.DateTimeField( 'processing started',
                        null = True )
    tEndStore   = models.DateTimeField( 'processing completed',
                        null = True )
    iItems      = models.PositiveIntegerField( 'items found',
                        null = True )
    iStoreItems = models.PositiveIntegerField( 'items stored',
                        null = True )
    iStoreUsers = models.PositiveIntegerField( 'stored for owner',
                        null = True )
    iItemHits   = models.PositiveIntegerField(
                        'have category, brand & model',
                        null = True )
    cResult     = models.TextField( 'search outcome', null = True )

    def __str__(self):
        return '%s - %s' % (
            getIsoDateTimeFromDateTime( self.tBegSearch ),
            self.iSearch.cTitle )

    class Meta:
        verbose_name_plural = 'searchlogs'
        db_table            = verbose_name_plural


