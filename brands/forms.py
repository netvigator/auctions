from django             import forms

from .models            import Brand

from core.validators    import gotTextOutsideParens

class BrandForm( forms.ModelForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super( BrandForm, self ).__init__( *args, **kwargs )
        self.fileds[ 'cTitle' ].validators.append( gotTextOutsideParens )
        
    class Meta:
        model = Brand
        fields = "__all__"