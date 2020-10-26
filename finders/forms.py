from django.forms       import ModelForm

from finders            import dItemFoundFields, dUserItemFoundUploadFields

from core.dj_import     import ValidationError
from core.forms         import BaseUserFinderKeeperFormGotCrispy

from .models            import ItemFound, UserItemFound

from ebayinfo.models    import EbayCategory

from pprint import pprint

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###


tItemFoundFields = tuple( dItemFoundFields.keys() )

class ItemFoundForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model       = ItemFound
        fields      = tItemFoundFields



tUserItemFoundUploadFields = tuple( dUserItemFoundUploadFields.keys() )

class UserItemFoundUploadForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model       = UserItemFound
        fields      = tUserItemFoundUploadFields




tUserItemFoundFields = (
    'iItemNumb',
    'iModel',
    'gModel',
    'iBrand',
    'iCategory',
    'bGetResult',
    'iSearch',
    'tTimeEnd',
    'iHitStars',
    'iUser' )


class UserItemFoundForm( BaseUserFinderKeeperFormGotCrispy ):

    class Meta:
        model       = UserItemFound
        fields      = tUserItemFoundFields

    def clean( self ):
        #
        if any( self.errors ):
            # Don't bother validating the formset unless each form is valid on its own
            print("in clean() but got field error")
            pprint( self.errors )
            #'iBrand': ['Select a valid choice. That choice is not one of the available choices.'],
            #'iHitStars': ['This field is required.'],
            #'iItemNumb': ['This field is required.'],
            #'iModel': ['Select a valid choice. That choice is not one of the available choices.'],
            #'iSearch': ['This field is required.'],
            #'iUser': ['Select a valid choice. That choice is not one of the available choices.'],
            #'tTimeEnd': ['This field is required.']}
            qsItems = ItemFound.objects.all()
            #print( 'ItemFound.objects.all() first object:', qsItems[0].iItemNumb )
            #print( 'self.instance.iItemNumb_id:', self.instance.iItemNumb_id )
            return
        #
        cleaned = super().clean()
        #

        iCleanModel     = cleaned["iModel"] or cleaned["gModel"] or None
        iCleanBrand     = cleaned["iBrand"]                      or None
        iCleanCategory  = cleaned["iCategory"]                   or None
        #
        iCleanModel     = iCleanModel.id    if iCleanModel    else None
        iCleanBrand     = iCleanBrand.id    if iCleanBrand    else None
        iCleanCategory  = iCleanCategory.id if iCleanCategory else None
        #
        # it is totally bizarre that django crashes without all the id's!!!
        #
        print("in clean()")
        if UserItemFound.objects.filter(
                iItemNumb_id    = self.instance.iItemNumb_id,
                iUser_id        = self.instance.iUser_id,
                iModel_id       = iCleanModel,
                iBrand_id       = iCleanBrand,
                iCategory_id    = iCleanCategory ).exists():
            #
            oUserItemFound = UserItemFound.objects.get(
                iItemNumb_id    = self.instance.iItemNumb_id,
                iUser_id        = self.instance.iUser_id,
                iModel_id       = iCleanModel,
                iBrand_id       = iCleanBrand,
                iCategory_id    = iCleanCategory )
            #
            if oUserItemFound.bListExclude: # hidden
                #
                oUserItemFound.bListExclude = False
                #
                oUserItemFound.save()
                #
                raise ValidationError(
                    'The hit already exists but was hidden, '
                    'it should now be visible',
                    code = 'exists_but_hidden' )
                #
            else:
                #
                raise ValidationError(
                    'The hit already exists',
                    code = 'exists' )
                #
            #
        #
        else:
            #
            print("did not find such a hit")
            pprint( self.instance.__dict__ )
            #print( 'self.instance.iItemNumb_id:', self.instance.iItemNumb_id )
            #print( 'self.instance.iUser_id    :', self.instance.iUser_id )
            #print( 'iCleanModel               :', iCleanModel )
            #print( 'iCleanBrand               :', iCleanBrand )
            #print( 'iCleanCategory            :', iCleanCategory )
            #
            qsUserItemsFound = UserItemFound.objects.all()
            if len( qsUserItemsFound ) > 0:
                for oUserItemFound in qsUserItemsFound:
                    oLast = oUserItemFound
                #
                print( 'last item:' )
                pprint( oLast.__dict__ )
                #
            else:
                print( 'no UserItemFound rows' )
        return cleaned


