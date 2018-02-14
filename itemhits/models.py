from django.db              import models
from djmoney.models.fields  import MoneyField
from django_countries.fields \
                            import CountryField

# Create your models here.

from models.models          import Model
from brands.models          import Brand
from categories.models      import Category

from django.contrib.auth import get_user_model
User = get_user_model()



class ItemImage(models.Model):
    iItemNumb       = models.BigIntegerField(
                        'ebay item number', primary_key = True )
    isequence       = models.PositiveSmallIntegerField( 'sequence' )
    cfilename       = models.CharField( 'local file name', max_length = 28 )
    coriginalurl    = models.TextField( 'original URL' )
    iUser           = models.ForeignKey( User, verbose_name = 'Owner' )
    tCreate         = models.DateTimeField( 'created on', auto_now_add= True )
    
    def __str__(self):
        return self.iItemNumb

    class Meta:
        verbose_name_plural = 'itemimages'
        db_table            = verbose_name_plural
        unique_together     = ('iItemNumb', 'isequence',)
#

