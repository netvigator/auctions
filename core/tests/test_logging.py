from logging            import getLogger

from core.utils_test    import TestCasePlus

logger = getLogger( 'test_logger' )


def throw_error_log():
    logger.error('an error')

def throw_message_log():
    logger.info('a message')


class LoggingTest( TestCasePlus ):

   def test_logging_error(self):

        with self.assertLogs( logger ='test_logger', level='ERROR') as cm:

            throw_error_log()

            self.assertIn(
                "ERROR:test_logger:an error",
                cm.output
            )

   def test_logging_info(self):

        with self.assertLogs( logger ='test_logger', level='INFO') as cm:

            throw_message_log()

            self.assertIn(
                "INFO:test_logger:a message",
                cm.output
            )
