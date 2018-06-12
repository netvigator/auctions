from crispy_forms.layout    import Submit

from core.forms             import ModelFormValidatesTitle
from .models                import Model

tModelFields = (
    'cTitle',
    'cLookFor',
    'bSubModelsOK',
    'iBrand',
    'bGenericModel',
    'iCategory',
    'cKeyWords',
    'iStars',
    'bMustHaveBrand',
    'bWanted',
    'bGetPictures',
    'bGetDescription',
    'cComment',
    'cExcludeIf',
    'cFileSpec1',
    'cFileSpec2',
    'cFileSpec3',
    'cFileSpec4',
    'cFileSpec5',
    )


class CreateModelForm( ModelFormValidatesTitle ):
    #

    def __init__( self, *args, **kwargs ):
        #
        super( CreateModelForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model   = Model
        fields  = tModelFields


class UpdateModelForm( ModelFormValidatesTitle ):
    #
    which = 'Update'

    def __init__( self, *args, **kwargs ):
        #
        super( UpdateModelForm, self ).__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #

    class Meta:
        model   = Model
        fields  = tModelFields
