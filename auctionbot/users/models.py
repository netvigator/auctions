from django.db              import models
from django.urls            import reverse

from core.dj_import         import AbstractUser, _

import pytz
from timezone_field         import TimeZoneField

from ebayinfo.models        import Market

iEbayUSA = Market.objects.get(
            cMarket = 'EBAY-US' ).pk or 0 # on error may need to comment out!

# iEbayUSA = 0 # uncomment this one if the above is causing migration error

class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name        = models.CharField(_('Name of User'), blank=True, max_length=255)
    #models.ForeignKey( Market, models.PositiveIntegerField(
    iEbaySiteID = models.ForeignKey( Market, on_delete=models.CASCADE,
                    verbose_name = 'ebay market (default)',
                    default = iEbayUSA )

    '''for testing, it is a big challenge to set default iEbaySiteID from markets table,
    because when testing, markets table starts out empty'''

    cCollection = models.CharField( 'Collection', max_length=80,  blank=True,
                    help_text = 'describe the collectables you are tracking' )
    cBio        = models.TextField( 'Bio info',   max_length=500, blank=True)
    cLocation   = models.CharField( 'Location',   max_length=30,  blank=True)
    zTimeZone   = TimeZoneField( default = 'UTC' )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_visiting_url(self):
        return reverse('visiting', kwargs={'pk': self.pk})

# 2021-07-23 change to non-sequential primary keys in psql on server
# ALTER TABLE users_user ALTER COLUMN id
# SET DEFAULT randomized(nextval('users_user_id_seq')::integer)::integer ;
