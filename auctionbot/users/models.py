from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers   import reverse
from django.db                  import models
from django.utils.encoding      import python_2_unicode_compatible
from django.utils.translation   import ugettext_lazy as _

import pytz
from timezone_field             import TimeZoneField

from ebayinfo.models            import Market

iEbayUSA = Market.objects.get(
            cMarket = 'EBAY-US' ).pk or 0 # on error may need to comment out!

# iEbayUSA = 0 # uncomment this one if the above is causing migration error

class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name        = models.CharField(_('Name of User'), blank=True, max_length=255)
    #models.ForeignKey( Market, models.PositiveIntegerField( 
    iMarket     = models.ForeignKey( Market,
                    verbose_name = 'ebay market (default)',
                    default = iEbayUSA, on_delete=models.CASCADE )

    '''for testing, it is a big challenge to set default iMarket from markets table,
    because when testing, markets table starts out empty'''
    
    cBio        = models.TextField( 'Bio info', max_length=500, blank=True)
    cLocation   = models.CharField( 'Location', max_length=30, blank=True)
    zTimeZone   = TimeZoneField( default = 'UTC' )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
