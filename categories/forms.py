from crispy_forms.layout    import Submit

from core.forms             import ModelFormValidatesTitle
from .models                import Category


tModelFields = (
    'cTitle',
    'cLookFor',
    'cKeyWords',
    'iStars',
    'bAllOfInterest',
    'bWantPair',
    'bAccessory',
    'bComponent',
    'iFamily',
    'cExcludeIf',
    'bModelsShared',
    )


class CreateCategoryForm( ModelFormValidatesTitle ):
    #
    
    def __init__( self, *args, **kwargs ):
        #
        super( CreateCategoryForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model   = Category
        fields  = tModelFields



class UpdateCategoryForm( ModelFormValidatesTitle ):
    #
    which = 'Update'

    def __init__( self, *args, **kwargs ):
        #
        super( UpdateCategoryForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model   = Category
        fields  = tModelFields
