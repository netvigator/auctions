from django             import forms

from core.crispy        import Field, Layout, Submit

from core.forms         import ModelFormValidatesTitle, tPossibleYears

from .models            import Model

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

tModelFields = (
    'cTitle',
    'bSubModelsOK',
    'cLookFor',
    'iModelYear',
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


def _getLayout():
    #
    return Layout(
            'cTitle',
            'bSubModelsOK',
            Field('cLookFor', rows='2'),
            'iModelYear',
            'iBrand',
            'bGenericModel',
            'iCategory',
            Field('cKeyWords', rows='2'),
            'iStars',
            'bMustHaveBrand',
            'bWanted',
            'bGetPictures',
            'bGetDescription',
            Field('cComment', rows='2'),
            Field('cExcludeIf', rows='2'),
            'cFileSpec1',
            'cFileSpec2',
            'cFileSpec3',
            'cFileSpec4',
            'cFileSpec5' )


class NewModelDataForm( ModelFormValidatesTitle ):
    #
    iModelYear = forms.ChoiceField(
            choices = tPossibleYears, required = False )

    class Meta:
        model   = Model
        fields  = tModelFields



class CreateModelForm( NewModelDataForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Add Model', css_class='btn-primary'))
        #
        self.helper.add_input(Submit('cancel', 'Cancel',
                                    css_class      = 'btn-primary',
                                    formnovalidate = 'formnovalidate' ) )
        #
        self.helper.layout = _getLayout()



class UpdateModelForm( NewModelDataForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        self.helper.add_input(Submit('submit', 'Save changes', css_class='btn-primary'))
        #
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.helper.layout = _getLayout()

