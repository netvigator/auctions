from django             import forms

from .models            import Category

from core.validators    import gotTextOutsideParens


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


class CategoryForm( forms.ModelForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super( CategoryForm, self ).__init__( *args, **kwargs )
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        
    class Meta:
        model   = Category
        fields  = tModelFields
