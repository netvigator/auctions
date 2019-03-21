from core.utils_test            import TestCasePlus

from ..templatetags.core_tags   import ( getDashForReturn,
                                         getDashForReturnButDropLast )

class GetDashForReturnTests( TestCasePlus ):
    '''get dash for return tests'''

    def test_get_dash_for_return(self):
        #
        s = 'abc\rdef\nghi\rklm'
        #
        sExpect = 'abc - def - ghi - klm'
        #
        self.assertEqual( getDashForReturn( s ), sExpect )


    def test_get_dash_for_return_but_drop_last(self):
        #
        s = 'abc\rdef\nghi\rklm'
        #
        sExpect = 'abc - def - ghi'
        #
        self.assertEqual( getDashForReturnButDropLast( s ), sExpect )

