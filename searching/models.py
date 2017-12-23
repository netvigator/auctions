from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

# not working: from django.utils.safestring import mark_safe

from ebaycategories.models import EbayCategory


class Search(models.Model):
    cTitle          = models.CharField( 'short description',
                                         max_length = 38, null = True )
    cKeyWords       = models.TextField(
        'search for key words (maximum length 350 characters)',
        max_length = 350 )
    # max length for a single key word is 98
    iEbayCategory   = models.ForeignKey( EbayCategory,
                                         verbose_name = 'ebay category (optional)',
                                         null = True, blank = True )
    cPriority       = models.CharField( 'processing priority',
                                         max_length = 2, null = True )
    tLastSearch     = models.DateTimeField( 'last search', null = True )
    cLastResult     = models.CharField( 'last search outcome',
                                         max_length = 28, null = True )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    tModify         = models.DateTimeField( 'updated on', auto_now    = True )

    def __str__(self):
        if EbayCategory.cTitle is None:
            return '%s: %s' % ( EbayCategory.cTitle, self.cKeyWords )
        else:
            return self.cKeyWords

    class Meta():
        verbose_name_plural = 'searches'
        db_table        = 'searching'
        unique_together = ('cKeyWords', 'iEbayCategory',)

    