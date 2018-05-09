'''
Django settings for Auction Shopping Bot project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
'''

import environ
import sys

from logging import getLogger

logger = getLogger(__name__)

from django.core.exceptions import ImproperlyConfigured

from django_countries.conf  import settings as countriesSettings

from Utils.Config import getConfMainIsDefaultHostnameVaries as getConf

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
]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'auctionbot.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'brands.apps.BrandsConfig',
    'categories.apps.CategoriesConfig',
    'models.apps.ModelsConfig',
    'ebayinfo.apps.EbayInfoConfig',
    'searching.apps.SearchingConfig',
    'archive.apps.ArchiveConfig',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auctions',
        'USER': 'secret',
        'PASSWORD': 'secret',
        'HOST': 'varies',
        'PORT': 'default',
    }
}

DATABASES['default']['USER'    ] = getSecret( 'POSTGRES_USER'    )
DATABASES['default']['PASSWORD'] = getSecret( 'POSTGRES_PASSWORD')
DATABASES['default']['HOST'    ] = getSecret( 'POSTGRES_HOST'    )
DATABASES['default']['PORT'    ] = getSecret( 'POSTGRES_PORT'    )


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
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
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
                'getIsoDateTime'    : 'core.templatetags.core_tags',
                'getNbsp'           : 'core.templatetags.core_tags',
                'model_name'        : 'core.templatetags.core_tags',
                'model_name_plural' : 'core.templatetags.core_tags',
                'field_name'        : 'core.templatetags.core_tags',}
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
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

########## CELERY
INSTALLED_APPS += ['auctionbot.taskapp.celery.CeleryConfig']

# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
CELERY_BROKER_URL = 'amqp://localhost' # using rabbitmq not redis

if CELERY_BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
########## END CELERY

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
TESTING = len(sys.argv) > 1 and 'test' in sys.argv[1]