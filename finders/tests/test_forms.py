from copy               import deepcopy

from django.urls        import reverse

from .base              import SetupUserItemsFoundAndUserFindersWebTest

from ..forms            import ( ItemFoundForm, UserItemFoundUploadForm,
                                 UserItemFoundForm )

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model

from ..models           import UserItemFound

from pprint import pprint

# need to test form validation for new hits & updated hits

# helpful:
# https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit




class TestAddingEditingUserHits( SetupUserItemsFoundAndUserFindersWebTest ):
    #

    def setUp( self ):
        #
        super().setUp()
        #





    def test_add_new_hit( self ):
        #
        '''
        qsModels = Model.objects.all()
        #
        if len( qsModels ) > 0:
            for oModel in qsModels:
                #
                print( oModel, oModel.iBrand, oModel.iCategory )
                #
        else:
            print( 'no models' )
        #
        models in table:

        470mF Digital Capacitor Checker
        601b Cadillac Manual
        Calais Cadillac Manual
        Fleetwood Cadillac Manual
        Model 2 Cadillac Manual

        properties in self:

        oBrand_hp Hewlett-Packard
        oBrand_GT Groove Tube
        oBrand Cadillac
        oCategory Manual

        oSearch My clever search 1

        oUserItemFound Digital Capacitance Tester Capacitor Meter Auto Range Multimeter Checker 470mF

        print()
        #
        for k, v in self.__dict__.items():
            if k and k.startswith( '_' ): continue
            print( k, v )
        '''
        #qsUserItemsFound = UserItemFound.objects.filter( iUser = self.user1 )
        #
        #print( 'UserItemsFound already in table:' )
        #for oUserItem in qsUserItemsFound:
            ##
            #print( ' ',
                   #oUserItem.iItemNumb,
                   #oUserItem.iHitStars,
                   #oUserItem.iSearch,
                   #'\n  Model:',
                   #oUserItem.iModel,
                   #'\n  Brand:',
                   #oUserItem.iBrand,
                   #'\n  Category:',
                   #oUserItem.iCategory )
            #
            # Digital Capacitance Tester Capacitor Meter Auto Range Multimeter Checker 470mF
            # 75
            # My clever search 1
            # Fleetwood
            # Cadillac
            # Manual
        #
        # webtest style
        #
        '''can add brand name not in there yet,
        cannot add a brand name already there'''
        #
        self.user = self.user1
        #
        oFleetwood = Model.objects.get(
                cTitle  = 'Fleetwood',
                iUser   = self.user1 )
        #




        o601b = Model.objects.get( cTitle = '601b',iUser = self.user1 )
        #
        dNewHit = dict(
                iItemNumb   = self.oUserItemFound.iItemNumb,
                iHitStars   = 5,
                iSearch     = self.oSearch,
                iModel      = None, # oFleetwood.id, form error on any model??
                iBrand      = self.oBrand,    # Cadillac
                iCategory   = self.oCategory, # manual
                iUser       = self.user1 )
        #
        oNewHit = UserItemFound( **dNewHit )
        oNewHit.save()
        #
        dFormData = dict(
                iItemNumb   = self.iItemNumb,
                iHitStars   = 5,
                iSearch     = self.oSearch,
                iModel      = None, # oFleetwood.id, form error on any model??
                iBrand      = self.oBrand.id,    # Cadillac
                iCategory   = self.oCategory.id, # manual
                iUser       = self.user1 )
        #
        sAddNewHitURL = reverse( 'finders:add' )
        #
        oForm = self.app.get( sAddNewHitURL ).form
        #
        oForm['iItemNumb'] = self.iItemNumb
        oForm['iHitStars'] = 5
        oForm['iSearch'  ] = self.oSearch
        oForm['iModel'   ] = ''
        oForm['iBrand'   ] = self.oBrand.id
        oForm['iCategory'] = self.oCategory.id
        oForm['iUser'    ] = self.user1


        form = UserItemFoundForm( data = dFormData )
        #
        print( 'in test_forms:', form['iItemNumb'].value() )
        #
        form.user    = self.user1 # need this!
        form.request = self.request
        #
        print( 'iBrand:', form['iBrand'].value() )
        print( Brand.objects.get( id = form['iBrand'].value() ) )
        print( 'self.user:', self.user )
        #
        print( 'Brands in form queryset:', form.fields["iBrand"].queryset )
        print( Brand.objects.filter( iUser = self.user ) )
        #
        if form.errors:
            print()
            print('form error(s):')
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        #
        form.is_valid()
        # self.assertTrue( form.is_valid() )
        # try again, this time with something different
        #
        '''
        #
        dFormData['iModel'] = o601b .id
        dFormData['iBrand'] = self.oBrand_hp.id
        #
        form = UserItemFoundForm( data = dFormData )
        #
        form.user    = self.user1 # need this!
        form.request = self.request
        #
        # form does not accept any model???
        #
        self.assertFalse( form.is_valid() )
        #
        #
        dFormData['iModel'] = None
        #
        form = UserItemFoundForm( data = dFormData )
        #
        form.user    = self.user1 # need this!
        form.request = self.request
        #
        self.assertTrue( form.is_valid() )
        #
        # form.save()
        #
        # try the same again
        #
        oCopyItem = deepcopy( self.oUserItemFound )
        #
        print( "oCopyItem.iModel:", oCopyItem.iModel )
        #
        oCopyItem.iModel = None
        #
        oCopyItem.save()
        #
        dFormData['iBrand'] = self.oBrand.id
        #
        form = UserItemFoundForm( data = dFormData )
        #
        form.user    = self.user1 # need this!
        form.request = self.request
        #
        self.assertFalse( form.is_valid() )
        #
        '''
        # this is what we already have, so form should block!
        #
        #dFormData = dict(
                #iItemNumb   = self.iItemNumb,
                #iHitStars   = 5,
                #iSearch     = self.oSearch,
                #iModel      = oFleetwood.id,
                #iBrand      = self.oBrand.id,    # Cadillac
                #iCategory   = self.oCategory.id, # manual
                #iUser       = self.user1 )


        ##print( 'self.oModel   :', self.oModel )
        ##print( 'self.oBrand   :', self.oBrand )
        ##print( 'self.oCategory:', self.oCategory )

        #form.request = self.request

        #self.assertFalse( form.is_valid() )

        #dErrors = dict( form.errors )
        ##
        #self.assertIn( 'iModel', dErrors )
        #self.assertEqual( len( dErrors ), 1 )
        #lMsg = ['Select a valid choice. '
                #'That choice is not one of the available choices.']
        #self.assertEqual( lMsg, dErrors['iModel'] )


        ##
        ##print( 'data before:' )
        ##pprint( dFormData )
        ###
        #dFormData = dict(
                #iItemNumb   = self.iItemNumb,
                #iHitStars   = 5,
                #iSearch     = self.oSearch,
                #iModel      = o601b.id,
                #iBrand      = self.oBrand.id,    # Cadillac
                #iCategory   = self.oCategory.id, # manual
                #iUser       = self.user1 )
        ##
        #form = UserItemFoundForm( data = dFormData )

        ##print( 'data after:' )
        ##pprint( dFormData )
        ###
        ###
        #form = UserItemFoundForm( data = dFormData )

        #form.request = self.request

        #self.assertTrue( form.is_valid() )
        #

