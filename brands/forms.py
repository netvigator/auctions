from core.forms         import ModelFormValidatesTitle
from django.forms       import ModelForm, formset_factory, BooleanField

from core.crispy        import Field, Layout, Submit
from .models            import Brand

from categories.models  import Category

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'cKeyWords',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )


def _getLayout():
    #
    return Layout(
            'cTitle',
            'bWanted',
            'bAllOfInterest',
            Field('cLookFor',  rows='2'),
            Field('cKeyWords', rows='2'),
            'iStars',
            Field('cComment',  rows='2'),
            'cNationality',
            Field('cExcludeIf',rows='2') )


class CreateBrandForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.form_tag = False
        #
        # using buttons in the template cuz want buttons below category list
        #
        #self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        #self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()

    class Meta:
        model  = Brand
        fields = tModelFields


class UpdateBrandForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.form_tag = False
        #
        # using buttons in the template cuz want buttons below category list
        #
        #self.helper.add_input(Submit('submit', 'Save changes', css_class='btn-primary'))
        #self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()
        #


    class Meta:
        model  = Brand
        fields = tModelFields


