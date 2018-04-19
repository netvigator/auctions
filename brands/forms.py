from core.forms             import ModelFormValidatesTitle
from django.forms           import ModelForm, formset_factory, BooleanField

from crispy_forms.layout    import Field, Layout, Submit
from .models                import Brand

from categories.models      import Category


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
        self.helper.form_tag = False
        #self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        #self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = Layout(
                'cTitle',
                'bWanted',
                'bAllOfInterest',
                'cLookFor',
                'iStars',
                'cComment',
                'cNationality',
                Field('cExcludeIf', rows='2') )

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

    class Meta:
        model  = Brand
        fields = tModelFields


