from django.test        import TestCase

from archive            import getListAsLines

from archive.tests      import s142766343340, s232742493872, s232709513135

from ..utils            import storeJsonSingleItemResponse


class GetListAsLinesTest( TestCase ):
    '''class for testing getListAsLines()'''

    def test_getListAsLines( self ):
        '''test getListAsLines()'''
        #
        #
        from archive.tests  import sPicList, sExpectList # in __init__.py
        #
        self.assertEqual( getListAsLines( sPicList ), sExpectList )


class SomeItemsTest( TestCase ):
    '''test some getSingleItem imports'''

    def test_s142766343340( self ):
        '''test getSingleItem 1946 Bendix Catalin'''
        #
        dGotItem = storeJsonSingleItemResponse( s142766343340 )

    def test_s232742493872( self ):
        '''test getSingleItem 1946 Bendix Catalin'''
        #
        dGotItem = storeJsonSingleItemResponse( s232742493872 )

    def test_s232709513135( self ):
        '''test getSingleItem 1946 Bendix Catalin'''
        #
        dGotItem = storeJsonSingleItemResponse( s232709513135 )

        