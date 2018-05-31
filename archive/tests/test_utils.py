import logging

from django.test        import TestCase

from archive            import getListAsLines

from archive.tests      import s142766343340, s232742493872, s232709513135

from ..models           import Item
from ..utils            import ( _storeJsonSingleItemResponse,
                                 getSingleItemThenStore )

from ..utils_test       import getSingleItemResponseCandidate

from searching.models   import ItemFound, UserItemFound
from searching.tests.test_stars import SetUpForKeyWordFindSearchHitsTests

from String.Get         import getTextAfter

logger = logging.getLogger(__name__)

logging_level = logging.INFO

''' prints logging messages to terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''

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
        iSavedRowID = _storeJsonSingleItemResponse( s142766343340 )
        #
        self.assertEqual( 142766343340, iSavedRowID )

    def test_s232742493872( self ):
        '''test getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        iSavedRowID = _storeJsonSingleItemResponse( s232742493872 )
        #
        self.assertEqual( 232742493872, iSavedRowID )

    def test_s232709513135( self ):
        '''test getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        iSavedRowID = _storeJsonSingleItemResponse( s232709513135 )
        #
        self.assertEqual( 232709513135, iSavedRowID )



class StoreItemsTest( TestCase ):
    '''test storing some getSingleItem imports in the table'''

    def test_s142766343340( self ):
        '''test storing getSingleItem 1946 Bendix Catalin including update'''
        #
        iOriginalSavedRowID = _storeJsonSingleItemResponse( s142766343340 )
        #
        self.assertTrue( Item.objects.filter( pk = 142766343340 ).exists() )
        #
        oItem = Item.objects.get( pk = 142766343340 )
        #
        self.assertEqual( oItem.iBidCount, 0 )
        #
        new142766343340 = s142766343340.replace( '"BidCount":0,', '"BidCount":5,' )
        #
        iNewSavedRowID = _storeJsonSingleItemResponse( new142766343340 )
        #
        oItem.refresh_from_db()
        #
        self.assertEqual( iOriginalSavedRowID, iNewSavedRowID )
        #
        self.assertEqual( oItem.iBidCount, 5 )


    def test_s232742493872( self ):
        '''test storing getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        iSavedRowID = _storeJsonSingleItemResponse( s232742493872 )
        #
        self.assertTrue( Item.objects.filter( pk = 232742493872 ).exists() )

    def test_s232709513135( self ):
        '''test storing getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        iSavedRowID = _storeJsonSingleItemResponse( s232709513135 )
        #
        self.assertTrue( Item.objects.filter( pk = 232709513135 ).exists() )


class GetAndStoreSingleItemsTests( SetUpForKeyWordFindSearchHitsTests ):
    '''class to test getSingleItemThenStore'''

    def test_get_single_active_item_then_store( self ):
        #
        d = getSingleItemResponseCandidate( bWantEnded = False )
        #
        iItemNumb = int( d[ 'iItemNumb' ] )
        #
        # need an ItemFound record here!
        #
        oItemFound = ItemFound.objects.all().first()
        #
        iOrigItemNumb = oItemFound.iItemNumb
        #
        oItemFound.iItemNumb = iItemNumb
        oItemFound.save()
        #
        if iOrigItemNumb is not None:
            oUserItemFound = UserItemFound.objects.get( iItemNumb = iOrigItemNumb )
            oUserItemFound.iItemNumb = oItemFound
            oUserItemFound.save()
        #
        getSingleItemThenStore( iItemNumb )
        #
        qsItem = Item.objects.filter( iItemNumb = iItemNumb )
        #
        self.assertEqual( len( qsItem ), 1 )


