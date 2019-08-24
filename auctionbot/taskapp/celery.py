from __future__             import absolute_import # celery absolutely needs this

import os
from logging                import getLogger

from sys                    import argv

from celery                 import Celery
from celery                 import shared_task

from django.apps            import apps, AppConfig
from django.conf            import settings

from config.settings.base   import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

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


@shared_task( bind = True, name = 'celery.debug_task' )
def debug_task(self):
    logger.debug('Request: {0!r}'.format(self.request) ) # pragma: no cover


# https://stackoverflow.com/questions/46530784/make-django-test-case-database-visible-to-celery/46564964#46564964
# assert 'celery.ping' in app.tasks

@shared_task( name = 'celery.ping' )
def ping():
    # type: () -> str
    """Pretty sophisticated task that brilliantly returns 'pong'."""
    return 'pong'

