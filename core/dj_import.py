# cannot import from here everywhere!
# you get circular import type problem if the importer is too low level!

from django.contrib.auth        import get_user_model
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.utils.encoding      import python_2_unicode_compatible
from django.core.exceptions     import ObjectDoesNotExist, ImproperlyConfigured
# django 2 made obsolete from django.core.urlresolvers   import reverse, resolve
# from django.urls                import reverse, resolve, reverse_lazy
from django.http.request        import HttpRequest
from django.utils.safestring    import mark_safe
from django.utils.translation   import ugettext_lazy as _
from django.views.generic       import DetailView, ListView
from django.views.generic       import RedirectView, UpdateView

from django_countries.conf      import settings as countriesSettings
from django_countries.fields    import CountryField

import xml.etree.ElementTree as ET
