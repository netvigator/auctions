from core.tests.base    import TestCasePlus

from ..utils            import _storeOneJsonItemInKeepers

from ..tests            import ( s142766343340,
                                 s232742493872,
                                 s232709513135 )

class StoreItemsTestPlusBase( TestCasePlus ):
    '''test storing some getSingleItem imports in the table'''

    def setUp( self ):
        #
        super( StoreItemsTestPlusBase, self ).setUp()
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


