from core.crispy    import Field, Layout, Submit
from core.forms     import ModelFormValidatesTitle

from .models        import Category

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

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


def _getLayout():
    #
    return Layout(
            'cTitle',
            Field('cLookFor', rows='2'),
            Field('cKeyWords', rows='2'),
            'iStars',
            'bAllOfInterest',
            'bWantPair',
            'bAccessory',
            'bComponent',
            'iFamily',
            Field('cExcludeIf', rows='2'),
            'bModelsShared' )

class CreateCategoryForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super( CreateCategoryForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()

    class Meta:
        model   = Category
        fields  = tModelFields



class UpdateCategoryForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super( UpdateCategoryForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()

    class Meta:
        model   = Category
        fields  = tModelFields
