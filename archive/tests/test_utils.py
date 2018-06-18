import logging

from datetime           import timedelta

from django.test        import TestCase
from django.utils       import timezone

from archive            import getListAsLines

from archive.tests      import ( s142766343340, s232742493872,
                                 s232709513135, s282330751118 )

from core.utils_test    import getEbayCategoriesSetUp

from ..models           import Item
from ..utils            import ( _storeJsonSingleItemResponse,
                                 getSingleItemThenStore,
                                 getItemsFoundForUpdate )

from ..utils_test       import getSingleItemResponseCandidate

from searching.models   import ItemFound, UserItemFound, Search
from searching.tests    import dSearchResult # in __init__.py
from searching.utils    import _storeUserItemFound, _storeItemFound

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
        t = _storeJsonSingleItemResponse( 142766343340, s142766343340 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertEqual( 142766343340, iSavedRowID )

    def test_s232742493872( self ):
        '''test getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        t = _storeJsonSingleItemResponse( 232742493872, s232742493872 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertEqual( 232742493872, iSavedRowID )

    def test_s232709513135( self ):
        '''test getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        t = _storeJsonSingleItemResponse( 232709513135, s232709513135 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertEqual( 232709513135, iSavedRowID )



class StoreItemsTest( TestCase ):
    '''test storing some getSingleItem imports in the table'''

    def test_s142766343340( self ):
        '''test storing getSingleItem 1946 Bendix Catalin including update'''
        #
        t = _storeJsonSingleItemResponse( 142766343340, s142766343340 )
        #
        iOriginalSavedRowID, sListingStatus = t
        #
        self.assertTrue( Item.objects.filter( pk = 142766343340 ).exists() )
        #
        oItem = Item.objects.get( pk = 142766343340 )
        #
        self.assertEqual( oItem.iBidCount, 0 )
        #
        new142766343340 = s142766343340.replace( '"BidCount":0,', '"BidCount":5,' )
        #
        t = _storeJsonSingleItemResponse( 142766343340, new142766343340 )
        #
        iNewSavedRowID, sListingStatus = t
        #
        oItem.refresh_from_db()
        #
        self.assertEqual( iOriginalSavedRowID, iNewSavedRowID )
        #
        self.assertEqual( oItem.iBidCount, 5 )


    def test_s232742493872( self ):
        '''test storing getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        t = _storeJsonSingleItemResponse( 232742493872, s232742493872 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertTrue( Item.objects.filter( pk = 232742493872 ).exists() )

    def test_s232709513135( self ):
        '''test storing getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        t = _storeJsonSingleItemResponse( 232709513135, s232709513135 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertTrue( Item.objects.filter( pk = 232709513135 ).exists() )


class GetAndStoreSingleItemsTests( SetUpForKeyWordFindSearchHitsTests ):
    '''class to test getSingleItemThenStore'''

    def test_get_single_active_item_then_store( self ):
        #
        d = getSingleItemResponseCandidate( bWantEnded = False )
        #
        if d is None: d = getSingleItemResponseCandidate()
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




class StoreSingleItemTests( getEbayCategoriesSetUp ):
    #
    ''' class for testing _storeItemFound() '''
    #

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super( StoreSingleItemTests, self ).setUp()
        #
        class ThisShouldNotBeHappening( Exception ): pass
        #
        sSearch         = "My clever search 1"
        self.oSearch    = Search( cTitle= sSearch, iUser = self.user1 )
        self.oSearch.save()
        #
        tBefore = timezone.now() - timezone.timedelta( days = 20 )
        #
        iItemNumb = _storeItemFound( dSearchResult, tBefore, {} )
        #
        if iItemNumb is None:
            raise ThisShouldNotBeHappening
        #
        _storeUserItemFound(
                dSearchResult,
                iItemNumb,
                tBefore,
                self.user1,
                self.oSearch.id )
        #
        self.iItemNumb  = iItemNumb
        self.tNow       = tBefore


    def test_store_fetched_single_item( self ):
        #
        oItemFound = ItemFound.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItemFound.cSellingState, 'Active' )
        #
        oUserItemFound = UserItemFound.objects.get(
                                iItemNumb_id = 282330751118 )
        #
        self.assertIsNone( oUserItemFound.tRetrieved )
        self.assertIsNone( oUserItemFound.tRetrieveFinal )
        #
        t = _storeJsonSingleItemResponse( 282330751118, s282330751118 )
        #
        iSavedRowID, sListingStatus = t
        #
        self.assertEqual( iSavedRowID, 282330751118 )
        #
        oItem = Item.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItem.cListingStatus, "Completed" )
        #
        self.assertEqual( oItem.cListingStatus, sListingStatus )
        #


    def test_store_item_found_fetched_single_item( self ):
        #
        getSingleItemThenStore( 282330751118, sContent = s282330751118 )
        #
        oItemFound = ItemFound.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItemFound.cSellingState, "Completed" )
        #

    def test_update_user_items_found_code( self ):
        #
        oUserItemFound = UserItemFound.objects.get(
                                iItemNumb_id = 282330751118 )
        #
        tNow = timezone.now()
        #
        getSingleItemThenStore( 282330751118,
                            sContent = s282330751118,
                            tNow     = tNow )
        #
        oItemFound = ItemFound.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItemFound.cSellingState, 'Completed' )
        #
        oUserItemFound = UserItemFound.objects.get(
                                iItemNumb_id = 282330751118 )
        #
        self.assertEqual( oUserItemFound.tRetrieved,    tNow )
        self.assertEqual( oUserItemFound.tRetrieveFinal,tNow )
        #
