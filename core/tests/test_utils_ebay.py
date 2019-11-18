from ..utils_ebay           import getValueOffItemDict
from ..utils_test           import AssertEmptyMixin, AssertNotEmptyMixin
from ..tests                import sResponse2ndCategoryItem

from core.utils_test        import TestCasePlus

from keepers                import dItemFields

from finders                import dItemFoundFields     # in __init__.py

from searching.tests        import sResponseItems2Test  # in __init__.py
from searching.utilsearch   import getSearchResultGenerator



class GetValueOffItemDictTests(
            AssertEmptyMixin, AssertNotEmptyMixin, TestCasePlus ):
    '''testing getValueOffItemDict()'''

    def dFieldsTester( self, dFields ):
        #
        '''tester - is supposed to be a tuple is actually a tuple?'''
        #
        for k, v in dFields.items():
            #
            self.assertIsInstance( v['t'], tuple )

    def test_dItemFoundFields( self ):
        #
        ''' testing the dItemFoundFields dict from finders'''
        #
        self.dFieldsTester( dItemFoundFields )

    def test_dItemFields( self ):
        #
        ''' testing the dItemFields dict from keepers'''
        #
        self.dFieldsTester( dItemFields )

    def test_get_value_off_item_dict( self, **kwargs ):
        #
        dFields     = dItemFoundFields
        getValue    = getValueOffItemDict
        #
        oItemIter = getSearchResultGenerator( '', 1, sResponseItems2Test )
        #
        dItem = next( oItemIter )
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertIsNotNone( dNewResult.get( 'iCategoryID' ) )
        #
        self.assertEqual( dNewResult.get( 'iCategoryID' ), 38034 )
        #
        self.assertEmpty( dNewResult.get( 'i2ndCategoryID' ) )
        #
        # galleryURL is optional
        #
        self.assertIsNotNone( dNewResult.get( 'cGalleryURL' ) )
        #
        self.assertNotEmpty( dNewResult.get( 'cGalleryURL' ) )
        #
        #
        # galleryURL is required but lots of legacy data d/n have
        #
        self.assertIsNotNone( dNewResult.get( 'iShippingType' ) )
        #
        self.assertEqual( dNewResult.get( 'iShippingType' ), 0 )
        #
        #
        #
        oItemIter = getSearchResultGenerator( '', 1, sResponse2ndCategoryItem )
        #
        #
        dItem = next( oItemIter )
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertIsNotNone( dNewResult.get( 'iCategoryID' ) )
        #
        self.assertEqual( dNewResult.get( 'iCategoryID' ), 170062 )
        #
        self.assertIsNotNone( dNewResult.get( 'i2ndCategoryID' ) )
        #
        self.assertEqual( dNewResult.get( 'i2ndCategoryID' ), 7275 )
        #
        self.assertEqual( dNewResult.get( 'cGalleryURL' ),
                         'http://thumbs2.ebaystatic.com/m/mgpbjxNWrOrRHjbTm5iC75w/140.jpg' )
        #
        # galleryURL is required but lots of legacy data d/n have
        #
        self.assertIsNotNone( dNewResult.get( 'iShippingType' ) )
        #
        self.assertEqual( dNewResult.get( 'iShippingType' ), 0 )
        #
        self.assertEqual( dNewResult.get( 'iHandlingTime' ), 1 )
        #
        #
        dItem = next( oItemIter )
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertIsNotNone( dNewResult.get( 'iCategoryID' ) )
        #
        self.assertEqual( dNewResult.get( 'iCategoryID' ), 50597 )
        #
        #
        self.assertEqual( dNewResult.get( 'cGalleryURL' ),
                         'http://thumbs2.ebaystatic.com/m/mAvNyg1TCZktrhVJMZZgiyw/140.jpg' )
        #
        # galleryURL is required but lots of legacy data d/n have
        #
        self.assertIsNotNone( dNewResult.get( 'iShippingType' ) )
        #
        self.assertEqual( dNewResult.get( 'iShippingType' ), 5 )
        #
        self.assertEmpty( dNewResult.get( 'iHandlingTime' ) )
        #
        #
        dItem = next( oItemIter )
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertIsNotNone( dNewResult.get( 'cSubTitle' ) )
        #
        self.assertEmpty( dNewResult.get( 'dBuyItNowPrice' ) )
        #
        dItem = next( oItemIter )
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertEqual( dNewResult.get( 'dBuyItNowPrice', 0 ), 3250.0 )
        #
