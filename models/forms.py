from django             import forms

from .models            import Model

from core.validators    import gotTextOutsideParens


tModelFields = (
    'cTitle',
    'cLookFor',
    'iBrand',
    'bGenericModel',
    'iCategory',
    'cKeyWords',
    'iStars',
    'bSubModelsOK',
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

class ModelForm( forms.ModelForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super( ModelForm, self ).__init__( *args, **kwargs )
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        
    class Meta:
        model   = Model
        fields  = tModelFields
