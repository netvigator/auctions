from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from markets.models import Market


iEbayUSA = Market.objects.get( cMarket = 'EBAY-US' ).id

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name        = models.CharField(_('Name of User'), blank=True, max_length=255)
    iMarket     = models.ForeignKey( Market,
                    verbose_name = 'ebay market (default)',
                    default = iEbayUSA )
    cBio        = models.TextField( 'Bio info', max_length=500, blank=True)
    cLocation   = models.CharField( 'Location', max_length=30, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
