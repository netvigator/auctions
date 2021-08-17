from django             import forms

from django.forms       import ModelForm, CheckboxInput

from core.crispy        import Field, Layout, Submit
from core.forms         import BaseModelFormGotCrispy
from core.dj_import     import ValidationError, ObjectDoesNotExist

# from crispy_forms.bootstrap import InlineRadios

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

from models.models      import Model

from searching          import getPriorityChoices, ALL_PRIORITIES

from .models            import Search
from .validators        import isPriorityValid

from ebayinfo.models    import EbayCategory



tSearchFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority',
    'bGetBuyItNows',
    'bInventory',
    'iMyCategory' )


def _getLayout():
    #
    return Layout(
            'cTitle',
            Field('cKeyWords', rows='2'),
            'iDummyCategory',
            'cPriority',
            'bGetBuyItNows',
            'bInventory',
            'iMyCategory' )


class BaseSearchForm( BaseModelFormGotCrispy ):
    '''
    using a form to get extra validation
    '''
    #
    cPriority = forms.ChoiceField(
            choices     = ALL_PRIORITIES,
            label       = Search._meta.get_field('cPriority').verbose_name,
            help_text   = Search._meta.get_field('cPriority').help_text )


    def __init__(self, *args, **kwargs):
        #
        self.bCreating = kwargs.get( 'instance' ) is None
        #
        super().__init__(*args, **kwargs)
        #
        self.fields[ 'cPriority' ].validators.append( isPriorityValid )
        #
        self.fields['cPriority'].choices = (
                getPriorityChoices( Search,
                                    self.user,
                                    self.instance.cPriority ) )
        #
        if self.instance and hasattr(self.instance, 'cPriority'):
            # print( 'self.instance' )
            self.initial['cPriority'] = self.get_initial_for_field(
                self.fields['cPriority'], 'cPriority')


    def clean(self):
        #
        cleaned         = super().clean()
        #
        sKeyWords       = cleaned.get( 'cKeyWords',     '' )
        #
        iDummyCategory  = cleaned.get( 'iDummyCategory', None )
        iDummyOriginal  = self.instance.iDummyCategory
        #
        iMyCategory     = cleaned.get( 'iMyCategory', None )
        #
        bCreating = self.bCreating
        #
        if bCreating and iDummyOriginal and not iDummyCategory:
            sMsg = 'Your ebay category "%s" is invalid' % iDummyOriginal
            raise ValidationError( sMsg, code='invalid ebay category' )
        #
        if not ( sKeyWords or iDummyCategory ):
            sMsg = 'key words or ebay category required (having both is OK)'
            raise ValidationError( sMsg, code='invalid' )
        #
        #print( 'iDummyCategory:', iDummyCategory )
        #print( 'iDummyOriginal:', iDummyOriginal )
        #
        if iMyCategory and not iDummyCategory:
            sMsg = '"My Category" is valid only if ebay category is set'
            raise ValidationError( sMsg, code='invalid' )
        #
        oEbayCategory = None
        #
        if ( self.user and iDummyCategory ):
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
            if oEbayCategory:
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
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()




class UpdateSearchForm( BaseSearchForm ):
    #
    '''form for editing existing search'''
    #

    def __init__(self, *args, **kwargs):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Save changes', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()



