from __future__     import absolute_import # celery absolutely needs this
import os
from logging        import getLogger

from celery         import Celery
from celery         import shared_task

from django.apps    import apps, AppConfig
from django.conf    import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

logger = getLogger(__name__)


app = Celery('auctionbot')

class CeleryConfig(AppConfig):
    name = 'auctionbot.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings' , namespace='CELERY' )
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

