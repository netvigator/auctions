from django.test        import TestCase
from django.utils       import timezone

from ..utils            import ( _getIsoDateTimeOffDateTimeCol,
                                 getReverseWithUpdatedQuery, getWhatsLeft )
from ..utils_testing    import getUrlQueryStringOff, queryGotUpdated

from Time               import sFormatISOdateTimeNoColon
from Time.Test          import isISOdatetime


class DateTimeTests(TestCase):
    '''date time function tests'''

    def test_getIsoDateTimeOffDateTimeCol(self):
        #
        '''test _getIsoDateTimeOffDateTimeCol()'''
        #
        oNow = timezone.now()
        #
        sNow = _getIsoDateTimeOffDateTimeCol( oNow )
        #
        self.assertTrue( isISOdatetime( sNow, sFormatISOdateTimeNoColon ) )
        
    def test_getReverseWithUpdatedQuery(self):
        #
        self.pk         = 1
        self.tModify    = timezone.now()
        #
        kwargs = { 'pk': self.pk, 'tModify': self.tModify }
        #
        sURL = getReverseWithUpdatedQuery( 'models:detail', kwargs = kwargs )
        #
        tParts = getUrlQueryStringOff( sURL )
        #
        self.assertEqual( tParts[0], '/models/%s/' % self.pk )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )

        
def textProcessingTests(TestCase):
    '''text processing tests'''

    def test_getWhatsLeft(self):
        #
        '''test getWhatsLeft()'''
        #
        s = 'This is for real (but not yet)'
        #
        self.assertEqual( getWhatsLeft(s), 'This is for real' )
        



        