import logging

from datetime           import timedelta
from os                 import listdir
from os.path            import dirname
from shutil             import rmtree
from time               import sleep

from django.test        import TestCase, tag
from django.utils       import timezone

from archive            import getListAsLines

from archive.tests      import ( s142766343340, s232742493872,
                                 s232709513135, s282330751118 )

from core.utils_test    import ( getEbayCategoriesSetUp, AssertEmptyMixin,
                                 AssertNotEmptyMixin )

from ..models           import Item
from ..utils            import ( _storeJsonSingleItemResponse,
                                 getSingleItemThenStore,
                                 getItemsFoundForUpdate,
                                 _getItemPicsSubDir,
                                 _getPicExtension,
                                 _getPicFileNameExtn,
                                 ITEM_PICS_ROOT,
                                 _getItemPicture,
                                 getItemPictures )

from ..utils_test       import getSingleItemResponseCandidate

from searching.models   import ItemFound, UserItemFound, Search
from searching.tests    import dSearchResult # in __init__.py
from searching.utils    import _storeUserItemFound, _storeItemFound

from searching.tests.test_stars import SetUpForKeyWordFindSearchHitsTests

from Dir.Test           import isDirThere
from File.Del           import DeleteIfExists
from File.Test          import isFileThere
from String.Get         import getTextAfter
from Web.Test           import isURL

logger = logging.getLogger(__name__)

logging_level = logging.INFO

''' prints logging messages to terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''

PIC_TEST_DIR = '/tmp/Item_Pictures'

class GetListAsLinesTest( TestCase ):
    '''class for testing getListAsLines()'''

    def test_getListAsLines( self ):
        '''test getListAsLines()'''
        #
        #
        from archive.tests  import sPicList, sExpectList # in __init__.py
        #
        self.assertEqual( getListAsLines( sPicList ), sExpectList )


class GeneratePathFileNameExtensionTests( AssertEmptyMixin, TestCase ):
    #
    sURL = ( 'https://i.ebayimg.com/00/s/OTAwWDE2MDA=/'
            'z/UTAAAOSwkV5aYX8~/$_57.JPG?set_id=8800005007' )
    #

    def test_get_pic_extension( self ):
        #
        self.assertEqual( _getPicExtension( self.sURL ), 'jpg' )
        #
        self.assertEmpty( _getPicExtension( 'xyz' ) )

    def test_get_item_pics_sub_dirs( self ):
        #
        iItemNumb = 253313715173
        #
        sSubDir = _getItemPicsSubDir( iItemNumb, '/tmp' )
        #
        self.assertEqual( sSubDir, '/tmp/25/33' )
        #
        self.assertTrue( isDirThere( sSubDir ) )
        #
        sOneUpDir = dirname( sSubDir )
        #
        if isDirThere( sOneUpDir ): rmtree( sOneUpDir )

    def test_get_pic_file_name_extn( self ):
        #
        iItemNumb = 253313715173
        #
        iSeq = 0
        #
        sPicFileNameExtn = _getPicFileNameExtn( self.sURL, iItemNumb, iSeq )
        #
        self.assertEqual( sPicFileNameExtn, '253313715173-00.jpg' )


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
        #



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


class GetAndStoreSingleItemsTests(
            AssertNotEmptyMixin, SetUpForKeyWordFindSearchHitsTests ):
    '''class to test getSingleItemThenStore'''

    def setUp( self ):
        #
        super( GetAndStoreSingleItemsTests, self ).setUp()
        #
        self.iItemNumb = None
        #
        for i in range(10): # do not want an infinite loop here!
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
                #
                qsUserItemFound = UserItemFound.objects.filter( iItemNumb = iOrigItemNumb )
                #
                for oUserItemFound in qsUserItemFound:
                    oUserItemFound.iItemNumb = oItemFound
                    oUserItemFound.save()
                #
            #
            getSingleItemThenStore( iItemNumb )
            #
            qsItems = Item.objects.filter( pk = iItemNumb )
            #
            if not qsItems: continue
            #
            oItem = qsItems[0]
            #
            lPicURLS = oItem.cPictureURLs.split()
            #
            if len( lPicURLS ) < 3: continue
            #
            for sPicURL in lPicURLS:
                #
                if isURL( sPicURL ):
                    #
                    self.iItemNumb = iItemNumb
                    #
                    break
                    #
                #
            #
        #

    def tearDown( self ):
        #
        pass
        #
        # if isDirThere( PIC_TEST_DIR ): rmtree( PIC_TEST_DIR )
        #

    @tag('ebay_api')
    def test_get_item_picture_hidden( self ):
        #
        iItemNumb = self.iItemNumb
        #
        oItem = Item.objects.get( iItemNumb = iItemNumb )
        #
        iSeq = 0
        #
        lPicURLS = oItem.cPictureURLs.split()
        #
        sItemPicsSubDir = _getItemPicsSubDir(
                                iItemNumb, PIC_TEST_DIR )
        #
        lResults = []
        #
        for sURL in lPicURLS:
            #
            if iSeq: sleep(1)
            #
            sResult = _getItemPicture( sURL, iItemNumb, sItemPicsSubDir, iSeq )
            #
            lResults.append( sResult )
            #
            iSeq += 1
            #
            if iSeq > 3: break
            #
        #
        for sResult in lResults:
            #
            self.assertTrue( isFileThere( sItemPicsSubDir, sResult ) )
            #
            DeleteIfExists( sItemPicsSubDir, sResult )
            #
        #
        if isDirThere( PIC_TEST_DIR ): rmtree( PIC_TEST_DIR )
        #

    @tag('ebay_api')
    def test_get_item_pictures_importable( self ):
        #
        iItemNumb = self.iItemNumb
        #
        oItem = Item.objects.get( iItemNumb = iItemNumb )
        #
        getItemPictures( iItemNumb, sItemPicsRoot = PIC_TEST_DIR )
        #
        oItem.refresh_from_db()
        #
        self.assertTrue( oItem.bGotPictures )
        #
        self.assertNotEmpty( oItem.tGotPictures )
        #
        self.assertGreater( oItem.iGotPictures, 2 )
        #
        sItemPicsDir = _getItemPicsSubDir( iItemNumb, PIC_TEST_DIR )
        #
        setFilesNames = frozenset( listdir( sItemPicsDir ) )
        #
        for iSeq in range( oItem.iGotPictures ):
            #
            sFileNameJPG = _getPicFileNameExtn( None, iItemNumb, iSeq, 'jpg' )
            sFileNamePNG = _getPicFileNameExtn( None, iItemNumb, iSeq, 'png' )
            #
            self.assertTrue( sFileNameJPG in setFilesNames or
                             sFileNamePNG in setFilesNames )


    def test_get_single_active_item_then_store( self ):
        #
        #
        qsItem = Item.objects.filter( iItemNumb = self.iItemNumb )
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
