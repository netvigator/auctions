
from core.tests.base                import TestCasePlus

from .celery                        import app, start_worker

from .tasks                         import add

class BatchSimulationTestCase( TestCasePlus ):
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

    def skip_test_my_function(self):
        # can hang unittests if celery not running
        add.delay( 8, 8 )



