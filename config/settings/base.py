'''
Django settings for Auction Shopping Bot project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
'''

import environ
import os
import sys

from logging            import getLogger

# cannot import from core.dj_import, get circular import error (sort of)
# from core.dj_import     import ImproperlyConfigured, countriesSettings
from django.core.exceptions     import ImproperlyConfigured
from django_countries.conf      import settings as countriesSettings

from pyPks.Utils.Config import getConfMainIsDefaultHostnameVaries as getConf

logger = getLogger(__name__)

dSecretsConf = getConf( 'Secrets.ini', tWantSections = ( 'email', 'sentry' ) )

# print( dSecretsConf )

ROOT_DIR = environ.Path(__file__) - 3  # (auctionbot/config/settings/base.py - 3 = auctionbot/)
APPS_DIR = ROOT_DIR.path('auctionbot')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    logger.warning( 'Loading : {}'.format(env_file) )
    env.read_env(env_file)
    logger.warning('The .env file has been loaded. See base.py for more information')


def getSecret( sSetting, sSection = None ):
    #
    '''Get the secret variable or return explicit exception.'''
    #
    sSetting = sSetting.lower()
    #
    try:
        #
        if sSection is None:
            return dSecretsConf[ sSetting ]
        else:
            return dSecretsConf[ sSection ][ sSetting ]
        #
    except KeyError:
        #
        if sSection is None:
            error_msg = 'Set the {0} environment variable'.format( sSetting )
        else:
            error_msg = (
                        'Set the {0} environment variable '
                        'under the {1} section'.format( sSetting, sSection ) )
        #
        raise ImproperlyConfigured(error_msg)



DJANGO_SECRET_KEY   = getSecret( 'DJANGO_SECRET_KEY')

SECRET_KEY          = DJANGO_SECRET_KEY
# django code is looking for SECRET_KEY

POSTGRES_PASSWORD   = getSecret( 'POSTGRES_PASSWORD')
POSTGRES_USER       = getSecret( 'POSTGRES_USER'    )
DATABASE_URL        = getSecret( 'DATABASE_URL'     )

# env['DJANGO_SECRET_KEY'] = DJANGO_SECRET_KEY
# TypeError: 'Env' object does not support item assignment


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'django_countries',
    'mptt',
    'admin_honeypot',
    'timezone_field',
#   'chroniker',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'auctionbot.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'ebayinfo.apps.EbayInfoConfig',
    'brands.apps.BrandsConfig',
    'categories.apps.CategoriesConfig',
    'models.apps.ModelsConfig',
    'searching.apps.SearchingConfig',
    'finders.apps.FindersConfig',
    'keepers.apps.KeepersConfig',
    'pyPks',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# see below for more!

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'auctionbot.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Rick Graves""", 'gravesricharde@yahoo.com'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : 'auctions',
        'USER'    : 'secret',
        'PASSWORD': 'secret',
        'HOST'    : 'varies',
        'PORT'    : 'default',
        'OPTIONS' : {},
    }
}

DATABASES['default']['USER'    ] = getSecret( 'POSTGRES_USER'    )
DATABASES['default']['PASSWORD'] = getSecret( 'POSTGRES_PASSWORD')
DATABASES['default']['HOST'    ] = getSecret( 'POSTGRES_HOST'    )
DATABASES['default']['PORT'    ] = getSecret( 'POSTGRES_PORT'    )

# these are needed to vaccum database on digitalocean
try:
    DATABASES['default']['ADMIN'   ] = getSecret( 'POSTGRES_ADMIN'   )
    DATABASES['default']['ADMIN_PW'] = getSecret( 'POSTGRES_ADMIN_PW')
except ImproperlyConfigured:
    DATABASES['default']['ADMIN'   ] = None
    DATABASES['default']['ADMIN_PW'] = None

# from pprint import pprint
# print( 'dSecretsConf:' )
# pprint( dSecretsConf )

try: # only required by digital ocean
    sslmode = getSecret( 'POSTGRES_SSLMODE' )
    if sslmode and sslmode == 'require':
        DATABASES['default']['OPTIONS' ] = {'sslmode': 'require'}
except ImproperlyConfigured:
    pass

# print( "DATABASES['default']['OPTIONS' ]:", DATABASES['default']['OPTIONS' ] )

DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

if 'time_zone' in dSecretsConf:
    #
    TIME_ZONE = dSecretsConf[ 'time_zone' ]


# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [ str(APPS_DIR.path('templates')), ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
            'libraries':{
                'sayListingType'    : 'core.tags.core_tags',
                'getDashForReturn'  : 'core.tags.core_tags',
                'getDashForReturnButDropLast' :
                                      'core.tags.core_tags',
                'getLineBreakForReturn' :
                                      'core.tags.core_tags',
                'model_name'        : 'core.tags.core_tags',
                'model_name_plural' : 'core.tags.core_tags',
                'field_name'        : 'core.tags.core_tags',
                'getLastDroppedFromCommaSeparatedString' :
                                      'finders.tags.finders_tags',
                }
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
#STATIC_ROOT = '/home/django/django_project/django_project/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [ str(APPS_DIR.path('static')) ]
# STATICFILES_DIRS = [ STATIC_ROOT ]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# Example: "http://media.example.com/"
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
# Example: "/var/www/example.com/media/"
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'auctionbot.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'auctionbot.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

#### CELERY ####

INSTALLED_APPS += ['auctionbot.taskapp.celery.CeleryConfig']

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#new-lowercase-settings

# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//' # using rabbitmq not redis
#broker_url = 'amqp://localhost' # using rabbitmq not redis
CELERY_BROKER_URL = 'redis://localhost:6379/0'

CELERY_TASK_DEFAULT_RATE_LIMIT = '1/s'
#task_default_rate_limit = '1/s'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Hong_Kong'

#### END CELERY

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^%s/' % dSecretsConf[ 'admin_url' ]

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

SESSION_COOKIE_SECURE = False # set to True in production

DATETIME_FORMAT = 'j N Y, P'
DATE_FORMAT     = 'j N Y'


countriesSettings.COUNTRIES_FIRST = [ 'US', 'GB' ]
countriesSettings.COUNTRIES_OVERRIDE = { 'US': 'United States',
                                         'AA': 'APO/FPO', # ebay allows this
                                         'AN':'Netherlands Antilles' }

# code can know if a test is being run
TESTING  = len(sys.argv) > 1 and 'test' in sys.argv[1] # settings
COVERAGE = '_' in os.environ and os.environ['_'].endswith( 'coverage' )


# 2021-04-17 getting a message on runnig tests after pip upgrade
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

AWS_STORAGE_BUCKET_NAME = 'auction-files'
AWS_ACCESS_KEY_ID       = getSecret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = getSecret('AWS_SECRET_KEY')
# AWS_STORAGE_BUCKET_NAME = 'auction-files' in base.py
# cannot include the AWS_STORAGE_BUCKET_NAME in the AWS_S3_ENDPOINT_URL!
# when doing collectstatic, get error:
# SSLError: SSL validation failed for
# https://auction-files.auction-files.sfo3.digitaloceanspaces.com/static/favicon.ico
# note auction-files is repeated in front
#AWS_S3_ENDPOINT_URL     = 'https://auction-files.sfo3.digitaloceanspaces.com'
#AWS_S3_CUSTOM_DOMAIN    = 'https://auction-files.sfo3.cdn.digitaloceanspaces.com'
# do do it this way:
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
