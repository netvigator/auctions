from django.forms       import ModelForm

from finders            import dItemFoundFields, dUserItemFoundUploadFields

from core.dj_import     import ValidationError
from core.forms         import BaseUserFinderKeeperForm

from .models            import ItemFound, UserItemFound

from ebayinfo.models    import EbayCategory

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###


tItemFoundFields = tuple( dItemFoundFields.keys() )

class ItemFoundForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model   = ItemFound
        fields  = tItemFoundFields




tUserItemFoundUploadFields = tuple( dUserItemFoundUploadFields.keys() )

class UserItemFoundUploadForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model   = UserItemFound
        fields  = tUserItemFoundUploadFields





tUserItemFoundFields = (
    'iModel',
    'gModel',
    'iBrand',
    'iCategory',
    'bGetResult',
    'iHitStars'  )


class UserItemFoundForm( BaseUserFinderKeeperForm ):

    class Meta:
        model   = UserItemFound
        fields  = tUserItemFoundFields

    def clean( self ):
        #
        if any( self.errors ):
            # Don't bother validating the formset unless each form is valid on its own
            return
        #
        cleaned = super().clean()
        #
        if UserItemFound.objects.filter(
                iItemNumb_id= self.instance.iItemNumb_id,
                iUser       = self.instance.iUser,
                iModel      = cleaned["iModel"] or cleaned["gModel"] or None,
                iBrand      = cleaned["iBrand"],
                iCategory   = cleaned["iCategory"]
                ).exists():
            #
            oUserItemFound = UserItemFound.objects.get(
                iItemNumb_id= self.instance.iItemNumb_id,
                iUser       = self.instance.iUser,
                iModel      = cleaned["iModel"] or cleaned["gModel"] or None,
                iBrand      = cleaned["iBrand"],
                iCategory   = cleaned["iCategory"] )
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
        return cleaned


