from core.forms import ModelFormValidatesTitle
from .models    import Brand


tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )


class BrandForm( ModelFormValidatesTitle ):
    #
    class Meta:
        model = Brand
        fields = tModelFields
