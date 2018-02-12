from core.forms import ModelFormValidatesTitle
from .models    import Category


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


class CategoryForm( ModelFormValidatesTitle ):
    #
    class Meta:
        model   = Category
        fields  = tModelFields
