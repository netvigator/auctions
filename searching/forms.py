from django                 import forms

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm, CheckboxInput

from crispy_forms.layout    import Field, Layout, Submit

from searching              import dItemFoundFields, dUserItemFoundUploadFields

from core.forms             import BaseModelFormGotCrispy

from models.models          import Model

from .models                import Search, ItemFound, UserItemFound
from .utilsearch            import getPriorityChoices, ALL_PRIORITIES
from .validators            import isPriorityValid

from ebayinfo.models        import EbayCategory



tSearchFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


class BaseSearchForm( BaseModelFormGotCrispy ):
    '''
    using a form to get extra validation
    '''
    which = 'Create' # can be over written
    #
    cPriority = forms.ChoiceField(
                    choices     = ALL_PRIORITIES,
                    label       = Search._meta.get_field('cPriority').verbose_name,
                    help_text   = Search._meta.get_field('cPriority').help_text )


    def __init__(self, *args, **kwargs):
        #
        if 'which' in kwargs:
            self.which = kwargs.pop('which')
        #
        super( BaseSearchForm, self ).__init__(*args, **kwargs)
        # BaseSearchForm, self
        #
        self.fields[ 'cPriority' ].validators.append( isPriorityValid )
        #
        self.fields['cPriority'].choices = (
                getPriorityChoices( Search,
                                    self.user,
                                    self.instance.cPriority ) )

        if self.instance and hasattr(self.instance, 'cPriority'):
            # print( 'self.instance' )
            self.initial['cPriority'] = self.get_initial_for_field(
                self.fields['cPriority'], 'cPriority')


    def clean(self):
        #
        cleaned = super( BaseSearchForm, self).clean()
        #
        sKeyWords       = cleaned.get( 'cKeyWords',     '' )
        #
        iDummyCategory  = cleaned.get( 'iDummyCategory', None )
        iDummyOriginal  = self.instance.iDummyCategory
        #
        bCreating = ( self.which == 'Create' )
        #
        if bCreating and iDummyOriginal and not iDummyCategory:
            sMsg = 'Your ebay category "%s" is invalid' % iDummyOriginal
            raise ValidationError( sMsg, code='invalid ebay category' )
            
        if not ( sKeyWords or iDummyCategory ):
            sMsg = 'key words or ebay category required (having both is OK)'
            raise ValidationError( sMsg, code='invalid' )
        
        #print( 'iDummyCategory:', iDummyCategory )
        #print( 'iDummyOriginal:', iDummyOriginal )
        #
        oEbayCategory = None
        #
        if (    self.user is not None and
                iDummyCategory is not None and iDummyCategory ):
            #
            try:
                oEbayCategory = EbayCategory.objects.get(
                    iEbaySiteID = self.user.iEbaySiteID,
                    iCategoryID = iDummyCategory )
            except ObjectDoesNotExist:
                sMsg = '"%s" is not an ebay category number!'
                raise ValidationError( sMsg,
                        params = ( iDummyCategory ),
                        code='ebay category number not found' )
            #
            cleaned['iEbayCategory'] = oEbayCategory
            #
        #
        #print( "cleaned['iEbayCategory']:", cleaned['iEbayCategory'] )
        #
        cPriority           = cleaned.get( 'cPriority' )
        #
        doCheckPriority = bCreating or self.instance.cPriority != cPriority
        #
        if doCheckPriority and (
            Search.objects.filter(
                iUser       = self.user,
                cPriority   = cPriority ).exists() ):
            #
            raise ValidationError('Priority "%s" already exists' % cPriority,
                        code='cPriority already exists' )
        #
        cTitle              = cleaned.get( 'cTitle' )
        #
        doCheckTitle = bCreating or self.instance.cTitle != cTitle
        #
        if doCheckTitle and (
            Search.objects.filter(
                iUser           = self.user ).filter(
                cTitle__iexact  = cTitle ).exists() ):
            #
            raise ValidationError('Title "%s" already exists' % cTitle,
                        code='title already exists' )
        
        #
        #
        doCheckSearch = (
                bCreating or
                self.instance.cKeyWords     != sKeyWords or
              ( self.instance.iEbayCategory != oEbayCategory.iCategoryID and
                oEbayCategory.iCategoryID > 0 ) )
        #
        if doCheckSearch:
            #
            sKeyWords           = cleaned.get( 'cKeyWords'      )
            oEbayCategory       = cleaned.get( 'iEbayCategory'  )
            #
            if oEbayCategory is not None:
                #
                if Search.objects.filter(
                        iUser               = self.user,
                        iEbayCategory       =
                            oEbayCategory.iCategoryID ).filter(
                        cKeyWords__iexact   = sKeyWords ).exists():
                    #
                    oEbayCategory = EbayCategory.get( iCategoryID = iEbayCategory )
                    #
                    raise ValidationError(
                        'You are already searching for "%s" in "%s"!' %
                        ( sKeyWords, oEbayCategory.name ),
                                code='already searching for keywords in ebay category' )
                #
            else: # oEbayCategory is None
                #
                if Search.objects.filter(
                        iUser     = self.user ).filter(
                        cKeyWords__iexact = sKeyWords ).exists():
                    #
                    raise ValidationError(
                        'You are already searching for "%s"!' % sKeyWords,
                                code='already searching for same keywords' )
                #
            #
            # really need to compare sets
            #
        #
        return cleaned

    class Meta:
        model   = Search
        fields  = tSearchFields



class CreateSearchForm( BaseSearchForm ):
    '''form for creating new search'''

    def __init__(self, *args, **kwargs):
        #
        super( CreateSearchForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #




class UpdateSearchForm( BaseSearchForm ):
    '''form for editing existing search'''
    which = 'Update' # can be over written
    #

    def __init__(self, *args, **kwargs):
        #
        super( UpdateSearchForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #



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



lUserItemFoundFields = [
    'iItemNumb.cTitle',
    'iItemNumb.cLocation',
    'iItemNumb.cCountry',
    'iItemNumb.cMarket', ]

tRest = (
    'iSearch',
    'tlook4hits',
    'cWhereCategory', )

tEditable = (
    'iModel',
    'iBrand',
    'iCategory',
    'bGetPictures',
    'iHitStars'  )


tUserItemFoundFields = tEditable
# tUserItemFoundFields.extend( tRest )



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
        if self.instance.iBrand is not None:
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
        if self.instance.iModel.bGenericModel:
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



