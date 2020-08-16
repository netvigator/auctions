from core.tests.base    import TestCasePlus

from ..utils            import getLastDropped


class TestGetLastDropped( TestCasePlus ):
    #
    def test_GetLastDropped( self ):
        #
        sOrig = ', '.join( map( str, range( 9 ) ) )
        #
        self.assertEqual(
                getLastDropped( sOrig ), '0, 1, 2, 3, 4, 5, 6, 7' )
        self.assertEqual(       sOrig,   '0, 1, 2, 3, 4, 5, 6, 7, 8' )
        #
