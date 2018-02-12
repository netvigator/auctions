from core.forms import ModelFormValidatesTitle
from .models    import Model

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

class ModelForm( ModelFormValidatesTitle ):
    #
    class Meta:
        model   = Model
        fields  = tModelFields
