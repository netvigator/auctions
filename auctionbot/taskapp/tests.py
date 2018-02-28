from celery.contrib.testing.worker  import start_worker
from django.test                    import SimpleTestCase

from .celery                        import app

from .tasks                         import add

class BatchSimulationTestCase(SimpleTestCase):
    allow_database_queries = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Start up celery worker
        cls.celery_worker = start_worker(app)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # Close worker
        cls.celery_worker.__exit__(None, None, None)

    def test_my_function(self):
        add.delay( 8, 8 )
        


