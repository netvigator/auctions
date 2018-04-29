from django.test        import TestCase

from ..models           import Item

from core.utils_test    import AssertEmptyMixin

from File.Get           import getListOffFileLines
from String.Get         import getTextBefore


class MakeSureAllFieldsAreInTableTest( AssertEmptyMixin, TestCase ):
    '''make sure all dItemFields are in the items table'''
    
    def test_make_sure_all_fields_are_in_table( self ):
        '''test to make sure all dItemFields are in the items table'''
        #
        lItemFields = [ getTextBefore( s, '= d(' ).strip()
                        for s
                        in getListOffFileLines( 'archive/__init__.py' )
                        if '= d( t' in s ]
        #
        self.assertGreater( len( lItemFields ), 20 )
        #
        lOmitted = [ s for s in lItemFields if not hasattr( Item, s ) ]
        #
        self.assertEmpty( lOmitted )


