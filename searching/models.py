from django.db                  import models
from django.core.urlresolvers   import reverse

# Create your models here.


from django.contrib.auth import get_user_model
User = get_user_model()

# not working: from django.utils.safestring import mark_safe

from ebaycategories.models import EbayCategory


class Search(models.Model):
    cTitle          = models.CharField( 'short description',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'search for key words (maximum length 350 characters) (required!)',
        max_length = 350,
        help_text = 'Bot will search for these words in the auction titles' )
    # max length for a single key word is 98
    iEbayCategory   = models.ForeignKey( EbayCategory,
                                verbose_name = 'ebay category (optional)',
                                null = True, blank = True,
        help_text = 'Limit search to items listed in this category (optional)' )
    cPriority       = models.CharField( 'processing priority',
                                max_length = 2, null = True,
        help_text = '1 is higher than 9, 9 is higher than A, A is higher than a' )
    tLastSearch     = models.DateTimeField( 'last search', null = True )
    cLastResult     = models.CharField( 'last search outcome',
                                max_length = 28, null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )

    def __str__(self):
        return self.cTitle

    class Meta():
        verbose_name_plural = 'searches'
        db_table        = 'searching'
        unique_together = ('cKeyWords', 'iEbayCategory',)

    def get_absolute_url(self):
        return reverse('searching:detail',
            kwargs={'pk': self.pk})
    