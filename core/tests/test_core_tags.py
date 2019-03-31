from core.utils_test            import TestCasePlus

from ..templatetags.core_tags   import ( getDashForReturn,
                                         getLineBreakForReturn,
                                         getDashForReturnButDropLast )

class GetDashForReturnTests( TestCasePlus ):
    '''get dash for return tests'''
    #
    s = 'abc\rdef\nghi\rklm'
    #

    def test_get_dash_for_return(self):
        #
        sExpect = 'abc - def - ghi - klm'
        #
        self.assertEqual( getDashForReturn( self.s ), sExpect )


    def test_get_dash_for_return_but_drop_last(self):
        #
        sExpect = 'abc - def - ghi'
        #
        self.assertEqual( getDashForReturnButDropLast( self.s ), sExpect )


    def test_get_line_break_for_return( self ):
        #
        sExpect = 'abc<BR>def<BR>ghi<BR>klm'
        #
        self.assertEqual( getLineBreakForReturn( self.s ), sExpect )
