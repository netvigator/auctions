import logging
import inspect

from datetime           import timedelta
from os                 import listdir
from os.path            import dirname
from shutil             import rmtree
from time               import sleep

from django.test        import tag
from django.utils       import timezone

from keepers            import getListAsLines

from core.utils_test    import ( GetEbayCategoriesWebTestSetUp,
                                 AssertEmptyMixin, AssertNotEmptyMixin,
                                 TestCasePlus )

from ..models           import Keeper
from ..tests            import ( s142766343340, s232742493872,
                                 s232709513135, s282330751118,
                                 s293004871422,
                                 s254154293727, s254130264753,
                                 s223348187115, s173696834267,
                                 s372536713027, s173696832184,
                                 s303000971114, s323589685342,
                                 sMissingItemIdErrorGotAck,
                                 sMadeUpErrorNoAck )
from ..utils            import ( _storeJsonSingleItemResponse,
                                 getSingleItemThenStore,
                                 getItemsFoundForUpdate,
                                 getItemPicsSubDir,
                                 _getPicExtension,
                                 _getPicFileNameExtn,
                                 ITEM_PICS_ROOT,
                                 _getItemPicture,
                                 getItemPictures,
                                 GetSingleItemNotWorkingError )

from ..utils_test       import getSingleItemResponseCandidate

from finders.models     import ItemFound, UserItemFound

from searching.models   import Search
from searching.tests    import dSearchResult # in __init__.py
from searching.utils    import _storeUserItemFound, _storeItemFound

from searching.tests.test_stars import SetUpForHitStarsWebTests

from pyPks.Dir.Test     import isDirThere
from pyPks.File.Del     import DeleteIfExists
from pyPks.File.Test    import isFileThere
from pyPks.String.Get   import getTextAfter
from pyPks.Web.Test     import isURL

logger = logging.getLogger(__name__)

logging_level = logging.INFO

''' prints logging messages to terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''

PIC_TEST_DIR = '/tmp/pictures_test_directory'

class GetListAsLinesTest( TestCasePlus ):
    '''class for testing getListAsLines()'''

    def test_getListAsLines( self ):
        '''test getListAsLines()'''
        #
        #
        from keepers.tests  import sPicList, sExpectList # in __init__.py
        #
        self.assertEqual( getListAsLines( sPicList ), sExpectList )


class GeneratePathFileNameExtensionTests( AssertEmptyMixin, TestCasePlus ):
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
        sSubDir = getItemPicsSubDir( iItemNumb, '/tmp' )
        #
        self.assertEqual( sSubDir, '/tmp/25/33/13/71' )
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


class SomeItemsTest( TestCasePlus ):
    '''test some getSingleItem imports'''

    def test_s142766343340( self ):
        '''test getSingleItem 1946 Bendix Catalin'''
        #
        t = _storeJsonSingleItemResponse( 142766343340, s142766343340 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        self.assertEqual( 142766343340, iSavedRowID )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_s232742493872( self ):
        '''test getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        t = _storeJsonSingleItemResponse( 232742493872, s232742493872 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        self.assertEqual( 232742493872, iSavedRowID )
        #
        oKeeper = Keeper.objects.get( iItemNumb = 232742493872 )
        #
        self.assertEqual( oKeeper.cCountry, 'RS' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_s232709513135( self ):
        '''test getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        t = _storeJsonSingleItemResponse( 232709513135, s232709513135 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        self.assertEqual( 232709513135, iSavedRowID )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



class StoreItemsTestPlus( TestCasePlus ):
    '''test storing some getSingleItem imports in the table'''

    def setUp( self ):
        #
        super( StoreItemsTestPlus, self ).setUp()
        #
        t = _storeJsonSingleItemResponse( 142766343340, s142766343340 )
        #
        self.iOriginalSavedRowID, sListingStatus, oItemFound = t
        #
        t = _storeJsonSingleItemResponse( 232742493872, s232742493872 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        t = _storeJsonSingleItemResponse( 232709513135, s232709513135 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_s142766343340( self ):
        '''test storing getSingleItem 1946 Bendix Catalin including update'''
        #
        self.assertTrue( Keeper.objects.filter( pk = 142766343340 ).exists() )
        #
        oItem = Keeper.objects.get( pk = 142766343340 )
        #
        self.assertEqual( oItem.iBidCount, 0 )
        #
        new142766343340 = s142766343340.replace( '"BidCount":0,', '"BidCount":5,' )
        #
        t = _storeJsonSingleItemResponse( 142766343340, new142766343340 )
        #
        iNewSavedRowID, sListingStatus, oItemFound = t
        #
        oItem.refresh_from_db()
        #
        self.assertEqual( self.iOriginalSavedRowID, iNewSavedRowID )
        #
        self.assertEqual( oItem.iBidCount, 5 )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_s232742493872( self ):
        '''test storing getSingleItem 1940's JAN 6SL7GT VT-229 AMPLIFER TUBES'''
        #
        #
        self.assertTrue( Keeper.objects.filter( pk = 232742493872 ).exists() )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_s232709513135( self ):
        '''test storing getSingleItem Fisher 400C 'Stereophonic' Tube Pre-Amplifier'''
        #
        self.assertTrue( Keeper.objects.filter( pk = 232709513135 ).exists() )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_missing_item( self ):
        #
        try:
            t = _storeJsonSingleItemResponse(
                    142766343340, sMissingItemIdErrorGotAck )
        except GetSingleItemNotWorkingError as e:
            self.assertIn(
                    'getSingleItem failure, check file', str( e ) )
        except Exception as e:
            self.fail('Unexpected exception raised:', e)
        else:
            self.fail( 'did not catch GetSingleItemNotWorkingError!' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_invalid_item( self ):
        #
        try:
            t = _storeJsonSingleItemResponse(
                    142766343340, sMadeUpErrorNoAck )
        except GetSingleItemNotWorkingError as e:
            self.assertIn(
                    'unexpected content from getSingleItem, check', str( e ) )
        except Exception as e:
            self.fail('Unexpected exception raised:', e)
        else:
            self.fail( 'did not catch GetSingleItemNotWorkingError!' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



class StoreSingleKeepersWebTests(
            AssertNotEmptyMixin, SetUpForHitStarsWebTests ):
    '''class to have some test keepers for other test classes'''

    def setUp( self ):
        #
        super( StoreSingleKeepersWebTests, self ).setUp()
        #
        d = {   293004871422 : s293004871422,
                254154293727 : s254154293727,
                254130264753 : s254130264753,
                223348187115 : s223348187115,
                173696834267 : s173696834267,
                372536713027 : s372536713027,
                173696832184 : s173696832184,
                303000971114 : s303000971114,
                323589685342 : s323589685342 }
        #
        for k, v in d.items():
            #
            getSingleItemThenStore( k, sContent = v )
            #
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
            qsItems = Keeper.objects.filter( pk = iItemNumb )
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

    def mark_all_finders_to_fetch_pictures( self ):
        # mark all UserItemFound rows to fetch pictures
        #
        UserItemFound.objects.all().update(
            bGetPictures = True,
            tRetrieved   = None )
        #
        # mark two UserItemFound rows as pictures already fetched
        qsAllItemsFound = ItemFound.objects.all().values_list(
                'iItemNumb', flat = True )
        #
        qsSomeUserItemNumbs = UserItemFound.objects.filter(
                iItemNumb__in = qsAllItemsFound )[:2].values_list(
                'iItemNumb', flat = True )
        #
        UserItemFound.objects.filter(
            iItemNumb__in = qsSomeUserItemNumbs ) .update(
                                    tRetrieved = timezone.now() )
        #
        # mark corresponding ItemFound row
        qsUserItemNumbs = ( UserItemFound.objects.filter(
                                bGetPictures        = True,
                                tRetrieved__isnull  = False )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        ItemFound.objects.filter(
                iItemNumb__in = qsUserItemNumbs ).update(
                                        tRetrieved = timezone.now() )
        #


def GetAndStoreSingleItemsWebTests( StoreSingleKeepersWebTests ):

    def test_getItemsFoundForUpdate( self ):
        #
        self.mark_all_finders_to_fetch_pictures()
        #
        qsUserItemNumbs = getItemsFoundForUpdate()
        #
        self.assertNotEmpty( qsUserItemNumbs )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_get_item_picture_hidden( self ):
        #
        iItemNumb = self.iItemNumb
        #
        oItem = Keeper.objects.get( iItemNumb = iItemNumb )
        #
        iSeq = 0
        #
        lPicURLS = oItem.cPictureURLs.split()
        #
        sItemPicsSubDir = getItemPicsSubDir(
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
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_get_item_pictures_importable( self ):
        #
        iItemNumb = self.iItemNumb
        #
        oItem = Keeper.objects.get( iItemNumb = iItemNumb )
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
        sItemPicsDir = getItemPicsSubDir( iItemNumb, PIC_TEST_DIR )
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
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_get_single_active_item_then_store( self ):
        #
        #
        qsItem = Keeper.objects.filter( iItemNumb = self.iItemNumb )
        #
        self.assertEqual( len( qsItem ), 1 )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



class StoreSingleItemTests( GetEbayCategoriesWebTestSetUp ):
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
        iItemNumb = _storeItemFound( dSearchResult, {} )
        #
        if iItemNumb is None:
            raise ThisShouldNotBeHappening
        #
        _storeUserItemFound(
                dSearchResult,
                iItemNumb,
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
        iSavedRowID, sListingStatus, oItemFound = t
        #
        self.assertEqual( iSavedRowID, 282330751118 )
        #
        oItem = Keeper.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItem.cListingStatus, "Completed" )
        #
        self.assertEqual( oItem.cListingStatus, sListingStatus )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_store_item_found_fetched_single_item( self ):
        #
        getSingleItemThenStore( 282330751118, sContent = s282330751118 )
        #
        oItemFound = ItemFound.objects.get( pk = 282330751118 )
        #
        self.assertEqual( oItemFound.cSellingState, "Completed" )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

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
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
