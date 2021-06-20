from os.path                import join

from django.utils           import timezone

from core.ebay_api_calls    import getApplicationToken

from core.tests.base        import AssertEmptyMixin, AssertNotEmptyMixin
from core.tests.base_class  import TestCasePlus

from ..models               import UserKeeper, Keeper

from ..utils                import ( _storeOneJsonItemInKeepers,
                                     getSingleItemThenStore )

from ..tests                import ( s142766343340,
                                     s232742493872,
                                     s232709513135,
                                     s293004871422,
                                     s254154293727,
                                     s254130264753,
                                     s223348187115,
                                     s173696834267,
                                     s372536713027,
                                     s173696832184,
                                     s303000971114,
                                     s323589685342,
                                     s164862306610 )

from finders.models         import ItemFound, UserFinder, UserItemFound

from searching.tests.base   import SetUpForHitStarsWebTests, getItemHitsLog

from pyPks.Numb.Get         import getRandomDigits
from pyPks.Time.Delta       import getIsoDateTimeNowPlus, getDeltaDaysFromISOs
from pyPks.Web.Test         import isURL


class NoExampleRecords( Exception ): pass


class StoreItemsTestPlusBase( TestCasePlus ):
    '''test storing some getSingleItem imports in the table'''

    def setUp( self ):
        #
        super().setUp()
        #
        t = _storeOneJsonItemInKeepers( 142766343340, s142766343340 )
        #
        self.iOriginalSavedRowID, sListingStatus, oItemFound = t
        #
        t = _storeOneJsonItemInKeepers( 232742493872, s232742493872 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        t = _storeOneJsonItemInKeepers( 232709513135, s232709513135 )
        #
        iSavedRowID, sListingStatus, oItemFound = t
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def tearDown( self ):
        #
        #UserKeeper.objects.all().delete()
        #Keeper.objects.all().delete()
        #ItemFound.objects.all().delete()
        #UserFinder.objects.all().delete()
        #UserItemFound.objects.all().delete()
        #
        pass
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class StoreSingleKeepersForWebTests( AssertNotEmptyMixin, AssertEmptyMixin,
            SetUpForHitStarsWebTests ):
    '''class to have some test keepers for other test classes'''

    def setUp( self ):
        #
        super().setUp()
        #
        self.oAuthToken = getApplicationToken()
        #
        d = {   293004871422 : s293004871422,
                254154293727 : s254154293727,
                254130264753 : s254130264753,
                223348187115 : s223348187115,
                173696834267 : s173696834267,
                372536713027 : s372536713027,
                173696832184 : s173696832184,
                303000971114 : s303000971114,
                323589685342 : s323589685342,
                164862306610 : s164862306610 }
        #
        iCount = 0
        #
        for k, v in d.items():
            #
            # populates UserKeeper, ports record from UserItemFound
            #
            # for testing, make some userFinders for another user HERE
            #
            if iCount % 3 == 0:
                #
                pass
                #
            #
            iCount += 1
            #
            getSingleItemThenStore( k, sContent = v )
            #
        #
        self.iItemNumb = None
        #
        for i in range(10): # do not want an infinite loop here!
            #
            d = self.getSingleItemResponseCandidate( bWantEnded = False )
            #
            if d is None: d = self.getSingleItemResponseCandidate()
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
            if iOrigItemNumb:
                #
                # qsUserItemFound = UserItemFound.objects.filter( iItemNumb = iOrigItemNumb )
                #
                # for oUserItemFound in qsUserItemFound:
                #     oUserItemFound.iItemNumb = oItemFound
                #     oUserItemFound.save()
                #
                qsUserFinder = UserKeeper.objects.filter( iItemNumb = iOrigItemNumb )
                #
                for oUserFinder in qsUserFinder:
                    oUserFinder.iItemNumb = oItemFound
                    oUserFinder.save()
                #
            #
            getSingleItemThenStore( iItemNumb, oAuthToken = self.oAuthToken )
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
        #UserKeeper.objects.all().delete()
        #Keeper.objects.all().delete()
        #ItemFound.objects.all().delete()
        #UserFinder.objects.all().delete()
        #UserItemFound.objects.all().delete()
        #
        # if isDirThere( ITEM_PICS_ROOT ): rmtree( ITEM_PICS_ROOT )
        #
        pass
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def getSingleItemResponseCandidate( self, bWantEnded = True ):
        #
        sStillAvailableDate = getIsoDateTimeNowPlus( -89 )
        #
        sHitLogFile = join( 'searching', 'tests', 'ItemHitsLog.log' )
        #
        def getActiveOrEnded( sDate ):
            #
            if bWantEnded:
                #
                bWantThis = int( getDeltaDaysFromISOs( sDate ) ) >= 1
                #
            else:
                #
                bWantThis = int( getDeltaDaysFromISOs( sDate ) ) <= -1
                #
            #
            return bWantThis
        #
        lItemHits = [ d for d in getItemHitsLog( sHitLogFile )
                    if ( d[ 'tTimeEnd' ] > sStillAvailableDate and
                        getActiveOrEnded( d[ 'tTimeEnd' ] ) ) ]
        #
        lPrioritySelect = []
        #
        for i in range( len( lItemHits ) ):
            #
            d = lItemHits[ i ]
            #
            iDaysAgo = int( getDeltaDaysFromISOs( d[ 'tTimeEnd' ] ) )
            #
            lPrioritySelect.append( ( iDaysAgo * 3 + int( d[ 'iHitStars' ] ), i ) )
            #
        #
        if not lPrioritySelect:
            #
            sayWhich = 'ended' if bWantEnded else 'active'
            #
            raise NoExampleRecords( 'no %s records in %s! Run live searching tests!' %
                                ( sayWhich, sHitLogFile ) )
            #
        #
        lPrioritySelect.sort()
        lPrioritySelect.reverse()
        #
        iTryThis = len( lPrioritySelect ) + 1
        #
        dTryThis = None
        #
        if lPrioritySelect:
            #
            for d in lItemHits:
                #
                while iTryThis > len( lPrioritySelect ):
                    #
                    iTryThis = int( getRandomDigits(1) )
                    #
                #
                if (    len( lPrioritySelect ) > iTryThis and
                        lPrioritySelect[ iTryThis ][1] < len( lItemHits ) ):
                    #
                    dTryThis = lItemHits[ lPrioritySelect[ iTryThis ][1] ]
                    #
                    break
                    #
                #
            #
        #
        # s = getSingleItem( dTryThis[ 'iItemNumb' ] )
        #
        return dTryThis


    def mark_all_finders_to_fetch_pictures( self ):
        # mark all UserItemFound rows to fetch pictures
        #
        # UserItemFound.objects.all().update(
        #     bGetResult  = True,
        #     tRetrieved   = None )
        #
        UserFinder.objects.all().update(
            bGetResult = True ) # aint got tRetrieved
        #
        # mark two UserItemFound rows as pictures already fetched
        qsAllItemsFound = ItemFound.objects.all().values_list(
                'iItemNumb', flat = True )
        #
        #
        # qsSomeUserItemNumbs = UserItemFound.objects.filter(
        #         iItemNumb__in = qsAllItemsFound )[:2].values_list(
        #         'iItemNumb', flat = True )
        #
        qsSomeUserFinderNumbs = UserFinder.objects.filter(
                iItemNumb__in = qsAllItemsFound )[:2].values_list(
                'iItemNumb', flat = True )
        #
        # UserItemFound.objects.filter(
        #     iItemNumb__in = qsSomeUserItemNumbs ) .update(
        #                             tRetrieved = timezone.now() )
        #
        UserFinder.objects.filter(
            iItemNumb__in = qsSomeUserFinderNumbs ).delete()
        #
        # mark corresponding ItemFound row
        # qsUserItemNumbs = ( UserItemFound.objects.filter(
        #                         bGetResult         = True,
        #                         tRetrieved__isnull  = False )
        #                     .values_list( 'iItemNumb', flat = True )
        #                     .distinct() )
        #
        qsUserFinderNumbs = ( UserFinder.objects.filter(
                                bGetResult = True )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        # ItemFound.objects.filter(
        #         iItemNumb__in = qsUserItemNumbs ).update(
        #                                 tRetrieved = timezone.now() )
        #
        ItemFound.objects.filter(
                iItemNumb__in = qsUserFinderNumbs ).update(
                                        tRetrieved = timezone.now() )
        #
