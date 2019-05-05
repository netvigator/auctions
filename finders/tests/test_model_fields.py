
from ..models           import ItemFound

from core.utils_test    import AssertEmptyMixin, TestCasePlus


from File.Get           import getListOffFileLines
from String.Get         import getTextBefore


class MakeSureAllFieldsAreInTableTest( AssertEmptyMixin, TestCasePlus ):
    '''make sure all dItemFields are in the items table'''

    def test_make_sure_all_fields_are_in_table( self ):
        '''test to make sure all dItemFields are in the items table'''
        #
        lLines = getListOffFileLines( 'searching/__init__.py' )
        #
        lItemsFoundLines = []
        #
        for s in lLines:
            #
            if s.startswith( 'dUserItemFoundUploadFields' ):
                break
            #
            lItemsFoundLines.append( s )
            #

        lItemFields = [ getTextBefore( s, '= d(' ).strip()
                        for s
                        in lItemsFoundLines
                        if '= d( t' in s ]
        #
        self.assertGreater( len( lItemFields ), 20 )
        #
        lOmitted = [ s for s in lItemFields if not hasattr( ItemFound, s ) ]
        #
        self.assertEmpty( lOmitted )



