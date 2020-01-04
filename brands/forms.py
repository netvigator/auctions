from core.forms         import ModelFormValidatesTitle
from django.forms       import ModelForm, formset_factory, BooleanField

from core.crispy        import Field, Layout, Submit
from .models            import Brand

from categories.models  import Category


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
        super( CreateBrandForm, self ).__init__( *args, **kwargs )
        #
        self.helper.form_tag = False
        #self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        #self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()

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
        self.helper.form_tag = False
        #self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        #self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()
        #


    class Meta:
        model  = Brand
        fields = tModelFields


