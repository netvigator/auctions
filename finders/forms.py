from django                 import forms

from django.forms           import ModelForm

from crispy_forms.layout    import Field, Layout, Submit

from finders                import dItemFoundFields, dUserItemFoundUploadFields

from core.forms             import BaseModelFormGotCrispy

from models.models          import Model

from .models                import ItemFound, UserItemFound

from ebayinfo.models        import EbayCategory



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
    'bGetPictures',
    'iHitStars'  )


class UserItemFoundForm( BaseModelFormGotCrispy ):
    #
    '''using a form on the edit user item found page'''
    #
    gModel = forms.ChoiceField( (),
                    label='Generic Models '
                          '(more than one brand may offer this model)' )


    def __init__( self, *args, **kwargs ):
        #
        super( UserItemFoundForm, self ).__init__( *args, **kwargs )
        #
        if self.instance.iBrand:
            self.fields["iModel"].queryset = (
                    Model.objects.filter(
                            iUser  = self.user,
                            iBrand = self.instance.iBrand ) )
        else:
            self.fields["iModel"].queryset = Model.objects.filter(
                                              iUser = self.user )

        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.fields['gModel'].choices = (
                ( o.pk, o.cTitle )
                  for o in Model.objects.filter(
                            iUser  = self.user,
                            bGenericModel = True) )
        #
        self.fields['gModel'].required = False
        #
        # model could be None
        if self.instance.iModel and self.instance.iModel.bGenericModel:
            #
            self.fields['gModel'].initial = self.instance.iModel_id
            #
        #
        self.helper.layout = Layout(
                'iModel',
                'gModel',
                'iBrand',
                'iCategory',
                'bGetPictures',
                Field( 'iHitStars', readonly = True ), )

    def clean( self ):
        #
        if any( self.errors ):
            # Don't bother validating the formset unless each form is valid on its own
            return
        #
        cleaned = super( UserItemFoundForm, self ).clean()
        #
        igModel = self.cleaned_data['gModel']
        iModel  = self.cleaned_data['iModel']
        #
        if iModel is None and igModel is not None:
            #
            self.cleaned_data['iModel'] = Model.objects.get( pk = igModel )
            #
        #
        return cleaned

    class Meta:
        model   = UserItemFound
        fields  = tUserItemFoundFields




