from django.db          import models

from core.utils         import getReverseWithUpdatedQuery

from ebayinfo.models    import EbayCategory

from categories.models  import Category

from core.dj_import     import get_user_model
User = get_user_model()

from searching          import ALL_PRIORITIES

from pyPks.Time.Output  import getIsoDateTimeFromDateTime


# ### models can be FAT but not too FAT! ###



class Search(models.Model):
    cTitle          = models.CharField( 'short description',
        help_text = 'This is just a short description -- ebay will not search for this<br>'
                    'you must have a) key word(s) and/or b) an ebay category',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'key words -- search for these (maximum length 350 characters)',
        max_length = 350, null = True, blank = True,
        help_text = 'What you type here will go into the ebay search box '
                    '-- mulitple terms will result in an AND search '
                    '(ebay will look for all terms).<br>'
                    'search for red OR green handbags as follows: '
                    'handbags (red,green)<br>'
                    'TIPS: to exclude words, put a - in front '
                    '(without any space),<br>'
                    'search handbags but exclude red as follows: '
                    'handbags -red<br>'
                    'search for handbags but '
                    'exclude red and green as follows: handbags -red -green' )
    # max length for a single key word is 98
    #models.ForeignKey( EbayCategory, models.PositiveIntegerField(
    iEbayCategory   = models.ForeignKey( EbayCategory,
                        on_delete=models.CASCADE,
                        verbose_name = 'ebay category',
                        null = True, blank = True,
        help_text = 'Limit search to items listed in this category' )
    # ### after updating ebay categories, check whether        ###
    # ### searches that were connected are still connected !!! ###
    iDummyCategory  = models.PositiveIntegerField( 'ebay category number',
                                null = True, blank = True,
        help_text = 'Limit search to items listed in this category<br>'
                    'copy the category number from ebay and paste here!!! (sorry)' )
    cPriority       = models.CharField( 'processing priority',
                                max_length = 2, null = True,
                                choices = ALL_PRIORITIES,
        help_text = 'high priority A1 A2 A3 ... Z9 low priority' )
    bGetBuyItNows   = models.NullBooleanField(
                    "also get 'Buy It Nows' (fixed price non auctions)?",
        help_text = 'You may get an avalanche of useless junk '
                    'if you turn this on -- be careful!',
                                blank = True, null = True,
                                default = False )
    bInventory    = models.NullBooleanField(
                    "also get 'Store Inventory' "
                    "(fixed price items in ebay stores)?",
        help_text = 'You may get an avalanche of useless junk '
                    'if you turn this on -- be careful!',
                                blank = True, null = True,
                                default = False )
    iMyCategory     = models.ForeignKey( Category,
                        on_delete=models.DO_NOTHING,
                        verbose_name = 'my category that matches ebay category',
                        null = True, blank = True,
        help_text = 'Example: if you have a category for "Manuals" and '
                    'this search is in the ebay category "Vintage Manuals" '
                    'put your "Manuals" category here.<br>If you have a '
                    'category "Widgets" and this search finds an item '
                    'with "Widget Manual" in the title, the bot will know '
                    'this item is for a manual, NOT a widget.')
    tBegSearch      = models.DateTimeField( 'last search started',
                                           null = True )
    tEndSearch      = models.DateTimeField( 'last search completed',
                                           null = True )
    cLastResult     = models.TextField( 'last search outcome', null = True )
    iUser           = models.ForeignKey( User, on_delete=models.CASCADE,
                                          verbose_name = 'Owner' )
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
    iSearch     = models.ForeignKey( Search, on_delete=models.CASCADE,
                        verbose_name = 'Search that first found this item' )
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
    cStoreDir   = models.CharField( 'search files directory',
                                max_length = 10,
                                null = True, blank = True )
    def __str__(self):
        sSayDir = ( self.cStoreDir
                    if self.cStoreDir
                    else getIsoDateTimeFromDateTime( self.tBegSearch ) )
        return '%s - %s' % ( sSayDir, self.iSearch.cTitle )

    class Meta:
        verbose_name_plural = 'searchlogs'
        db_table            = verbose_name_plural


