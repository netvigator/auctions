"""
Production Configurations

- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis for cache

- Use sentry for error logging


"""

# boto deprecated, now they recommend boto3
# from boto.s3.connection import OrdinaryCallingFormat

import logging

logger = logging.getLogger(__name__)

from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
# SECRET_KEY = env('DJANGO_SECRET_KEY')
# set in base.py


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# raven sentry client
# See https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.io/
WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE
RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS',
                         default=[ '147.182.255.231',
                                   'localhost',
                                   'auctionshoppingbot.com',
                                   '*',
                                   'antei.xyz'] ) # latter is for sentry
# '*' https://stackoverflow.com/questions/54133995/how-to-resolve-err-connection-refused-when-connecting-to-virtualenv-django-runni
# END SITE CONFIGURATION

# INSTALLED_APPS += ['gunicorn', ]


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID       = getSecret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = getSecret('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = getSecret('AWS_BUCKET_NAME')
#AWS_S3_ENDPOINT_URL    = 'https://auction-files.sfo3.digitaloceanspaces.com'
#AWS_S3_CUSTOM_DOMAIN   = 'https://auction-files.sfo3.cdn.digitaloceanspaces.com'
AWS_S3_ENDPOINT_URL     = 'https://sfo3.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN    = 'https://sfo3.cdn.digitaloceanspaces.com'
AWS_DEFAULT_ACL         = 'public-read'
AWS_AUTO_CREATE_BUCKET  = True
AWS_QUERYSTRING_AUTH    = False
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_LOCATION            = 'static'

# AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat() # comes from boto3, deprecated

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
# update 2019-05-12
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
control = 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY)
#AWS_HEADERS = {
    #'Cache-Control': bytes(control, encoding='latin-1')
#}
AWS_S3_OBJECT_PARAMETERS = { 'CacheControl': control }

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
# Example: "http://media.example.com/"
# MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_URL = '/home/django/django_project/django_project/media/'
MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'media')

# Example: "/var/www/example.com/media/"
# MEDIA_ROOT = '/home/django/django_project/django_project/media/'
MEDIA_ROOT = 'media/'

# Static Assets
# ------------------------
# from whitenoise.storage import CompressedManifestStaticFilesStorage

'''
did not work

class laxCompressedManifestStaticFilesStorage( CompressedManifestStaticFilesStorage ):
    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        # `filename` is the name of file to hash if `content` isn't given.
        # `name` is the base name to construct the new hashed filename from.
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        if filename:
            filename = urlsplit(unquote(filename)).path.strip()
        filename = filename or clean_name
        opened = False
        if content is None:
            try:
                content = self.open(filename)
            except IOError:
                # Handle directory paths and fragments
                return name
            opened = True
        try:
            file_hash = self.file_hash(clean_name, content)
        finally:
            if opened:
                content.close()
        path, filename = os.path.split(clean_name)
        root, ext = os.path.splitext(filename)
        if file_hash:
            file_hash = ".%s" % file_hash
        hashed_name = os.path.join(path, "%s%s%s" %
                                   (root, file_hash, ext))
        unparsed_name = list(parsed_name)
        unparsed_name[2] = hashed_name
        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        if '?#' in name and not unparsed_name[3]:
            unparsed_name[2] += '?'
        return urlunsplit(unparsed_name)

STATICFILES_STORAGE = 'laxCompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'CompressedManifestStaticFilesStorage'
'''
# STATIC_ROOT = '/home/django/django_project/django_project/'
# STATIC_ROOT = 'static/'


# STATIC_URL = '/static/'
# STATIC_ROOT = ROOT_DIR / 'staticfiles'
# STATICFILES_DIRS = (ROOT_DIR / 'static',)

# in base.py
# MEDIA_URL = '/media/'
# MEDIA_ROOT = ROOT_DIR / 'mediafiles'

STATIC_URL  = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'static')

# https://docs.djangoproject.com/en/3.2/howto/static-files/deployment/
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE= 'custom_storages.MediaStorage'

# hard coded path, will surely change when server moves!
# STATICFILES_DIRS.append( '/home/django/django_project/django_project/static/' )
STATICFILES_DIRS = [ STATIC_ROOT ]


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL   = env('DJANGO_DEFAULT_FROM_EMAIL',
            default='Auction Shopping Bot <noreply@auctionshoppingbot.com>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX',
            default='[Auction Shopping Bot]')
SERVER_EMAIL         = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ['anymail', ]
#ANYMAIL = {
    #'MAILGUN_API_KEY': env('DJANGO_MAILGUN_API_KEY'),
    #'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')

ANYMAIL = {
    'MAILGUN_API_KEY': getSecret( 'MAILGUN_API_KEY', 'email' ),
    'MAILGUN_SENDER_DOMAIN': 'mg.auctionshoppingbot.com'
}

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
# DATABASES['default'] = env.db('DATABASE_URL')
# configured in base.py

# CACHING
# ------------------------------------------------------------------------------

#REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0)
## Heroku URL does not pass the DB number, so we parse it in
#CACHES = {
    #'default': {
        #'BACKEND': 'django_redis.cache.RedisCache',
        #'LOCATION': REDIS_LOCATION,
        #'OPTIONS': {
            #'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            #'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        ## http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        #}
    #}
#}


# Sentry Configuration
# SENTRY_DSN = env('DJANGO_SENTRY_DSN')

SENTRY_DSN = getSecret( 'SENTRY_DSN', 'sentry' )

SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT',
                    default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', ],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', ],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', ],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry', ],
            'propagate': False,
        },
    },
}
SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
    'DSN': SENTRY_DSN
}

# Custom Admin URL, use {% url 'admin:index' %}
# ADMIN_URL = env('DJANGO_ADMIN_URL')
# set in base.py for all

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

