from core.crispy    import Field, Layout, Submit
from core.forms     import ModelFormValidatesTitle
from core.mixins    import SetUserNeedsModelYearsMixin

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
    'bModelsByYear',
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
            'bModelsShared',
            'bModelsByYear' )

class NewCategoryDataForm(
            SetUserNeedsModelYearsMixin, ModelFormValidatesTitle ):

    def __init__( self, *args, **kwargs ):
        #
        # request is a custom parameter!!! see the view mixin
        # can crash django code if there!!!
        #
        self.request = kwargs.pop( 'request', None )
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(
                Submit( 'cancel', 'Cancel', css_class='btn-primary' ) )
        #

    class Meta:
        model   = Category
        fields  = tModelFields

    def clean( self ):
        #
        if any( self.errors ): return
        #
        cleaned = super().clean()
        #
        if  ( self.request is not None and
              self['bModelsByYear'].value and
              hasattr( self.request, 'user' ) ):
            #
            self.setUserNeedsModelYears( self.request.user, True )
            #
        #
        return cleaned


class CreateCategoryForm( NewCategoryDataForm ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(
                Submit( 'submit', 'Create', css_class='btn-primary' ) )
        #
        self.helper.layout = _getLayout()


class UpdateCategoryForm( NewCategoryDataForm ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(
                Submit( 'submit', 'Save Changes', css_class='btn-primary' ) )
        #
        self.helper.layout = _getLayout()
