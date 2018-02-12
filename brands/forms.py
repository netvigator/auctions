from django             import forms

from .models            import Brand

from core.validators    import gotTextOutsideParens


tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )


class BrandForm( forms.ModelForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super( BrandForm, self ).__init__( *args, **kwargs )
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        
    class Meta:
        model = Brand
        fields = tModelFields
