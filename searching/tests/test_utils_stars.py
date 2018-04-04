from os.path            import join

from django.core.urlresolvers import reverse

from django.test        import RequestFactory
from django.utils       import timezone

from core.utils_test    import ( setUpBrandsCategoriesModels,
                                 SetupViewForTestingMixin )

from searching          import RESULTS_FILE_NAME_PATTERN

from ..models           import ( ItemFound, UserItemFound,
                                 ItemFoundTemp )
from ..tests            import sResponseSearchTooBroad
from ..utils            import storeSearchResultsInDB

from .test_utils        import ( GetBrandsCategoriesModelsSetUp,
                                 storeSearchResultsTestsSetUp )

from ..utils_stars      import ( _getModelRegExFinders4Test,
                                 _getCategoryRegExFinders4Test,
                                 _getBrandRegExFinders4Test,
                                 getFoundItemTester,
                                 findSearchHits )

from brands.views       import BrandUpdateView
from models.models      import Model

from File.Del           import DeleteIfExists
from File.Write         import QuietDump



class KeyWordFindSearchHitsTests(GetBrandsCategoriesModelsSetUp):
    #
    ''' class for testing storeSearchResultsInDB() store records '''
    #
    def setUp(self):
        #
        #print( 'will call super' )
        super( KeyWordFindSearchHitsTests, self ).setUp()
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
            ( 'EBAY-US', self.user1.username, self.oSearch.id, '000' ) )
        #
        #print( 'will DeleteIfExists' )
        DeleteIfExists( '/tmp', self.sExampleFile )
        #
        #print( 'will QuietDump' )
        QuietDump( sResponseSearchTooBroad, self.sExampleFile )
        #
        t = ( storeSearchResultsInDB(   self.oSearchLog.id,
                                        self.sMarket,
                                        self.user1.username,
                                        self.oSearch.id,
                                        self.oSearch.cTitle ) )
        #
        iCountItems, iStoreItems, iStoreUsers = t
        #
        #print( '\n' )
        #print( 'setting up KeyWordFindSearchHitsTests' )

    def test_find_search_hits(self):
        #
        ''' test _storeUserItemFound() with actual record'''
        #
        findSearchHits( self.user1.id, bCleanUpAfterYourself = False )
        #
        oTempItemsFound = ItemFoundTemp.objects.all()
        #
        self.assertEquals( len( oTempItemsFound ), 72 )
        #
        oUserItems = UserItemFound.objects.filter(
                        iUser = self.user1 ).order_by( '-iHitStars' )
        #
        iCount = 0
        #
        for oTemp in oUserItems:
            #
            #print( '\n' )
            ##
            if oTemp.iHitStars == 0: break
            ##
            #sSayModel = sSayBrand = sSayCategory = ''
            ##
            #if oTemp.iModel:
                #sSayModel = oTemp.iModel.cTitle
            #if oTemp.iBrand:
                #sSayBrand = oTemp.iBrand.cTitle
            #if oTemp.iCategory:
                #sSayCategory = oTemp.iCategory.cTitle
            
            #print( 'Auction Title:', oTemp.iItemNumb.cTitle )

            #print( 'ItemNumb     :', oTemp.iItemNumb.pk     )
            #print( 'iHitStars    :', oTemp.iHitStars        )
            #print( 'Model        :', sSayModel              )
            #print( 'Brand        :', sSayBrand              )
            #print( 'Category     :', sSayCategory           )
            ##
            #print( 'Search       :', oTemp.iSearch.cTitle   )
            #print( 'WhereCategory:', oTemp.cWhereCategory   )
            #print( 'Evaluated    :',
                  #oTemp.tlook4hits.strftime('%Y-%m-%d %H:%M:%S'))
            #print( 'Auction End  :', oTemp.iItemNumb.tTimeEnd)
            #
            iCount += 1
        #
        #
        self.assertEquals( iCount, 72 )
        #
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_BrandsCategoriesModels_setUp(self):
        #
        iCount = Model.objects.all().count()
        #
        self.assertEqual( iCount, 151 )
        #


 

class findersStorageTest( setUpBrandsCategoriesModels ):
    
    #
    ''' test Finder Storage for Brands, Categories & Models '''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #
    def test_BrandRegExFinderStorage(self):
        #
        t = _getBrandRegExFinders4Test( self.oBrand )
        #
        findTitle, findExclude = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_CategoryRegExFinderStorage(self):
        #
        t = _getCategoryRegExFinders4Test( self.oCategory )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



    def test_ModelRegExFinderStorage(self):
        #
        t = _getModelRegExFinders4Test( self.oModel )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #

    def testBrandGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oBrand.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oBrand.cRegExLook4Title,
                                    ( 'Cadillac|Caddy', 'Caddy|Cadillac') )
        #
        self.assertEquals( self.oBrand.cRegExExclude, 'golf' )
        #
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



    def testCategoryGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oCategory, dFinders )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oCategory.pk ]
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oCategory.cRegExLook4Title,
                                        ( 'Gizmo|Widget', 'Widget|Gizmo' ) )
        #
        self.assertEquals( self.oCategory.cRegExExclude,  'Delta'  )
        self.assertEquals( self.oCategory.cRegExKeyWords, 'Gadget' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def testModelGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oModel, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oModel.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oModel.cRegExLook4Title,
                                ( 'Woodie|Fleetwood', 'Fleetwood|Woodie' ) )
        #
        self.assertEquals( self.oModel.cRegExExclude,  'golf'     )
        self.assertEquals( self.oModel.cRegExKeyWords, 'Eldorado' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class EditingTitleShouldBlankFinder(
            SetupViewForTestingMixin, setUpBrandsCategoriesModels ):
    #
    ''' test WereAnyReleventRegExColsChangedMixin'''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #
    

    def test_change_cTitle_blank_finder( self ):
        #
        ''' test WereAnyReleventRegExColsChangedMixin'''
        #
        self.client.login(username ='username1', password='mypassword')
        #
        form = self.app.get(reverse('account_login')).form
        form['username'] = 'username1'
        form['password'] = 'mypassword'
        response = form.submit().follow()
        self.assertEqual(response.context['user'].username, 'username1')
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        bInTitle, bExcludeThis = foundItem( self.oBrand.cTitle )
        #
        self.assertIn(     self.oBrand.cRegExLook4Title,
                                    ( 'Cadillac|Caddy', 'Caddy|Cadillac') )
        #
        data = { k : v for ( k,v ) in self.oBrand if v is not None }
        #
        data[ 'cLookFor' ] = ''
        #
        kwargs = { 'pk' : self.oBrand.id }
        #
        factory = RequestFactory()
        #
        # Create the request
        request = factory.get( reverse( 'brands:edit', kwargs = kwargs ) )
        request.user = self.user1
        #
        v = self.setup_view( BrandUpdateView(), request, data = data )
        #
        # response = BrandUpdateView.as_view( request )
        #
        form = v.get_form()
        #
        # form.save(commit=False)
        # form.save_m2m()
        #
        # self.assertTrue( v.form_valid( form ) )
        # AttributeError: 'UpdateBrandForm' object has no attribute 'cleaned_data'
        #
        #
        # self.assertIsNotNone( form.instance.cRegExLook4Title )
        #
        v.redoRegEx( form )
        #
        self.assertIsNone( form.instance.cRegExLook4Title )
        #
        # self.assertIsNone( self.oBrand.cRegExLook4Title )
        #
        update_url = reverse( 'brands:edit', args=(self.oBrand.id,) )
        #
        print( 'update_url:', update_url )
        # GET the form
        r = self.client.get(update_url)
        #
        form = r.context['form']
        data = form.initial # form is unbound but contains data
        #
        # manipulate some data
        data['cLookFor'] = ''
        #
        # POST to the form
        r = self.client.post(update_url, data)
        #
        # retrieve again
        r = self.client.get(update_url)
        #
        self.assertEqual(r.context['form'].initial['cLookFor'], '')
        #
        print( self.app.get( update_url ) )
        #form = self.app.get( update_url ).form
        ##
        #self.assertEqual(form['cLookFor'].value, 'Caddy')
        ##
        #self.assertIn( form['cRegExLook4Title'].value, 
                                #( 'Cadillac|Caddy', 'Caddy|Cadillac') )
        ##
        #form['cLookFor'] = ''
        ##
        #response = form.submit()
        ##
        #self.assertIsNone( form['cRegExLook4Title'].value )
        #



