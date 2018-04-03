from crispy_forms.layout    import Submit

from core.forms             import ModelFormValidatesTitle
from .models                import Brand


tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )


class CreateBrandForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super( CreateBrandForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model  = Brand
        fields = tModelFields


class UpdateBrandForm( ModelFormValidatesTitle ):
    #
    which = 'Update'

    def __init__( self, *args, **kwargs ):
        #
        super( UpdateBrandForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model  = Brand
        fields = tModelFields
