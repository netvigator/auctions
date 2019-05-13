from django.contrib.auth        import get_user_model
from django.core.exceptions     import ObjectDoesNotExist, ImproperlyConfigured
from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest
from django.utils.safestring    import mark_safe

from django_countries.conf      import settings as countriesSettings


import xml.etree.ElementTree as ET
