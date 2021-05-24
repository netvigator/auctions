from __future__             import absolute_import # celery absolutely needs this

import os
from logging                import getLogger

from sys                    import argv

#from celery                import Celery, shared_task
#from celery.contrib.testing.worker  import start_worker

from django.apps            import apps, AppConfig
from django.conf            import settings

from config.settings.base   import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# ### begin workaround ###
# 2021-05-24 celery not working, so giving up on it!
# instead, will set nice level on cron job processes
# will leave the celery structure in place, to allow retrying later if desired

from pyPks.Object.Get       import Null

start_worker            = Null()

class Celery( Null ):

    conf                = Null()
    config_from_object  = Null()
    autodiscover_tasks  = Null()

    def __init__( self, *args, **kwargs ):
        #
        super( Celery, self ).__init__( **kwargs )

# ### end workaround ###

sConfig = 'config.settings.production'

for sArg in argv:
    if sArg.startswith( '--config=' ):
        sConfig = sArg[ len( '--config=' ) : ]
        break

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', sConfig ) # pragma: no cover

logger = getLogger(__name__)


app = Celery('auctionbot',
            backend = CELERY_RESULT_BACKEND,
            broker  = CELERY_BROKER_URL )


# https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/
app.conf.task_create_missing_queues = True

# https://medium.com/@taylorhughes/three-quick-tips-from-two-years-with-celery-c05ff9d7f9eb
CELERYD_TASK_SOFT_TIME_LIMIT = 600

class CeleryConfig(AppConfig):
    name            = 'auctionbot.taskapp'
    verbose_name    = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # app.config_from_object('django.conf:settings' , namespace='CELERY' )
        app.config_from_object( 'django.conf:settings' )
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'OPBEAT'): # obsolete

            from opbeat.contrib.django.models import client as opbeat_client
            from opbeat.contrib.django.models import logger as opbeat_logger
            from opbeat.contrib.django.models \
                import register_handlers as opbeat_register_handlers
            from opbeat.contrib.celery import register_signal as opbeat_register_signal


            try:
                opbeat_register_signal(opbeat_client)
            except Exception as e:
                opbeat_logger.exception(
                    'Failed installing celery hook: %s' % e)

            if 'opbeat.contrib.django' in settings.INSTALLED_APPS:
                opbeat_register_handlers()


# @shared_task( bind = True, name = 'celery.debug_task' )
def debug_task(self):
    logger.debug('Request: {0!r}'.format(self.request) ) # pragma: no cover


# https://stackoverflow.com/questions/46530784/make-django-test-case-database-visible-to-celery/46564964#46564964
# assert 'celery.ping' in app.tasks

# @shared_task( name = 'celery.ping' )
def ping():
    # type: () -> str
    """Pretty sophisticated task that brilliantly returns 'pong'."""
    return 'pong'

