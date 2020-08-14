from copy                   import deepcopy

from django.urls            import reverse
from django.test            import RequestFactory

from core.dj_import         import HttpRequest

from .base                  import SetUpBrandsCategoriesModelsWebTest

from ..mixins               import GetPaginationExtraInfoInContext
from ..views                import ListViewGotModel

from finders.views          import FinderIndexView

from searching.utils_stars  import _getFoundItemTester
from searching.tests.base   import SetUpForHitStarsWebTests

from pyPks.Dict.Maintain    import purgeNoneValueItems
from pyPks.Object.Get       import QuickObject


class TestPagination( SetUpForHitStarsWebTests ):
    '''class to test pagination thoroughly'''

    def setUp( self ):
        #
        super().setUp()
        #
        self.factory = RequestFactory()
        #
        self.request = self.factory.get(reverse(
                'finders:index' ) )
        #
        self.request.user = self.user1
        #
        self.view = FinderIndexView()
        #
        self.view.request = self.request



    def test_pagination_tests( self ):
        '''test pagination thoroughly'''
        #
        self.view.kwargs = { 'select' : 'A' } # testing glitch workaround

        self.view.object_list = self.view.get_queryset()

        context = self.view.get_context_data( object_list = range(1,10000) )

        oThisPage = deepcopy( context.get('page_obj') )
        #
        self.assertEqual( oThisPage.number, 1 )
        self.assertEqual( context.get( 'show_range' ), range(1,3) )
        self.assertEqual( context.get( 'iBeg'       ),   0 )
        self.assertEqual( context.get( 'iEnd'       ),   2 )
        self.assertEqual( context.get( 'iMidLeft'   ),   0 )
        self.assertEqual( context.get( 'iMidRight'  ),  50 )
        self.assertEqual( context.get( 'iMaxPage'   ), 100 )
        #
        oThisPage.number = 50
        #
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = '1' )
        #
        self.assertEqual( context.get( 'show_range' ), range(49,52) )
        self.assertEqual( context.get( 'iBeg'       ),  49 )
        self.assertEqual( context.get( 'iEnd'       ),  51 )
        self.assertEqual( context.get( 'iMidLeft'   ),  25 )
        self.assertEqual( context.get( 'iMidRight'  ),  75 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 25
        #
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(24,27) )
        self.assertEqual( context.get( 'iBeg'       ),  24 )
        self.assertEqual( context.get( 'iEnd'       ),  26 )
        self.assertEqual( context.get( 'iMidLeft'   ),  13 )
        self.assertEqual( context.get( 'iMidRight'  ),  37 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 13
        #
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(12,15) )
        self.assertEqual( context.get( 'iBeg'       ),  12 )
        self.assertEqual( context.get( 'iEnd'       ),  14 )
        self.assertEqual( context.get( 'iMidLeft'   ),   7 )
        self.assertEqual( context.get( 'iMidRight'  ),  19 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 7
        #
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range( 6, 9) )
        self.assertEqual( context.get( 'iBeg'       ),   6 )
        self.assertEqual( context.get( 'iEnd'       ),   8 )
        self.assertEqual( context.get( 'iMidLeft'   ),   4 )
        self.assertEqual( context.get( 'iMidRight'  ),  10 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 4
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range( 3, 6) )
        self.assertEqual( context.get( 'iBeg'       ),   3 )
        self.assertEqual( context.get( 'iEnd'       ),   5 )
        self.assertEqual( context.get( 'iMidLeft'   ),   2 )
        self.assertEqual( context.get( 'iMidRight'  ),  52 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 2
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range( 1, 4) )
        self.assertEqual( context.get( 'iBeg'       ),   0 )
        self.assertEqual( context.get( 'iEnd'       ),   3 )
        self.assertEqual( context.get( 'iMidLeft'   ),   0 )
        self.assertEqual( context.get( 'iMidRight'  ),  51 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 75
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(74,77) )
        self.assertEqual( context.get( 'iBeg'       ),  74 )
        self.assertEqual( context.get( 'iEnd'       ),  76 )
        self.assertEqual( context.get( 'iMidLeft'   ),  38 )
        self.assertEqual( context.get( 'iMidRight'  ),  87 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 87
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(86,89) )
        self.assertEqual( context.get( 'iBeg'       ),  86 )
        self.assertEqual( context.get( 'iEnd'       ),  88 )
        self.assertEqual( context.get( 'iMidLeft'   ),  81 )
        self.assertEqual( context.get( 'iMidRight'  ),  93 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 93
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(92,95) )
        self.assertEqual( context.get( 'iBeg'       ),  92 )
        self.assertEqual( context.get( 'iEnd'       ),  94 )
        self.assertEqual( context.get( 'iMidLeft'   ),  90 )
        self.assertEqual( context.get( 'iMidRight'  ),  96 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 96
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(95,98) )
        self.assertEqual( context.get( 'iBeg'       ),  95 )
        self.assertEqual( context.get( 'iEnd'       ),  97 )
        self.assertEqual( context.get( 'iMidLeft'   ),  94 )
        self.assertEqual( context.get( 'iMidRight'  ),  98 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 98
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(97,101) )
        self.assertEqual( context.get( 'iBeg'       ),  97 )
        self.assertEqual( context.get( 'iEnd'       ), 100 )
        self.assertEqual( context.get( 'iMidLeft'   ),  49 )
        self.assertEqual( context.get( 'iMidRight'  ),   0 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( 1 )
        #
        oThisPage.number = 50
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(49,52) )
        self.assertEqual( context.get( 'iBeg'       ),  49 )
        self.assertEqual( context.get( 'iEnd'       ),  51 )
        self.assertEqual( context.get( 'iMidLeft'   ),  25 )
        self.assertEqual( context.get( 'iMidRight'  ),  75 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 25
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(24,27) )
        self.assertEqual( context.get( 'iBeg'       ),  24 )
        self.assertEqual( context.get( 'iEnd'       ),  26 )
        self.assertEqual( context.get( 'iMidLeft'   ),  13 )
        self.assertEqual( context.get( 'iMidRight'  ),  37 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 13
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(12,15) )
        self.assertEqual( context.get( 'iBeg'       ),  12 )
        self.assertEqual( context.get( 'iEnd'       ),  14 )
        self.assertEqual( context.get( 'iMidLeft'   ),   7 )
        self.assertEqual( context.get( 'iMidRight'  ),  19 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 19
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(18,21) )
        self.assertEqual( context.get( 'iBeg'       ),  18 )
        self.assertEqual( context.get( 'iEnd'       ),  20 )
        self.assertEqual( context.get( 'iMidLeft'   ),  16 )
        self.assertEqual( context.get( 'iMidRight'  ),  59 )
        #print( "iMidLeft:    ", context.get( 'iMidLeft'   ) )
        #print( "iMidRight:   ", context.get( 'iMidRight'  ) )
        #
        sPrevPage = str( oThisPage.number )
        #
        oThisPage.number = 16
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,10000),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(15,18) )
        self.assertEqual( context.get( 'iBeg'       ),  15 )
        self.assertEqual( context.get( 'iEnd'       ),  17 )
        self.assertEqual( context.get( 'iMidLeft'   ),   8 )
        self.assertEqual( context.get( 'iMidRight'  ),  58 )
        #
        sPrevPage = None # str( oThisPage.number )
        #
        oThisPage.number = 1
        #
        #print('')
        #print('oThisPage.number:', oThisPage.number  )
        context = self.view.get_context_data(
                object_list = range(1,1770),
                page_obj    = oThisPage,
                sPrevPage   = sPrevPage )
        #
        self.assertEqual( context.get( 'show_range' ), range(1,3) )
        self.assertEqual( context.get( 'iBeg'       ),   0 )
        self.assertEqual( context.get( 'iEnd'       ),   2 )
        self.assertEqual( context.get( 'iMidLeft'   ),   0 )
        self.assertEqual( context.get( 'iMidRight'  ),   9 )
        #
        #print('')
        #print( "show_range  :", context.get( 'show_range' ) )
        #print( "iBeg        :", context.get( 'iBeg'       ) )
        #print( "iEnd        :", context.get( 'iEnd'       ) )
        #print( "iMidLeft    :", context.get( 'iMidLeft'   ) )
        #print( "iMidRight   :", context.get( 'iMidRight'  ) )
        #print( "iMaxPage    :", context.get( 'iMaxPage'   ) )



class EditingTitleShouldBlankFinder( SetUpBrandsCategoriesModelsWebTest ):
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
        self.loginWebTest()
        #
        dFinders  = {}
        #
        foundItem = _getFoundItemTester( self.oBrand, dFinders )
        #
        t = foundItem( self.oBrand.cTitle )
        #
        # sInTitle, uGotKeyWordsOrNoKeyWords, uExcludeThis = t
        #
        self.assertIn( self.oBrand.cRegExLook4Title,
                            ( r'Cadillac|\bCaddy\b', r'\bCaddy\b|Cadillac') )
        #
        update_url = reverse( 'brands:edit', args=(self.oBrand.id,) )
        #
        # GET the form
        r = self.client.get( update_url )
        #
        form = r.context['form']
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cLookFor'], 'Caddy')
        #
        purgeNoneValueItems( data )
        #
        # manipulate some data
        data['cLookFor'] = ''
        #
        # POST to the form
        r = self.client.post(update_url, data)
        #
        # retrieve again
        r = self.client.get( update_url )
        #
        self.assertEqual(r.context['form'].initial['cLookFor'], '')
        #
        form = self.app.get( update_url ).form
        #
        form['cLookFor'] = ''
        #
        response = form.submit()
        #
        self.oBrand.refresh_from_db()
        #
        self.assertIsNone( self.oBrand.cRegExLook4Title )



