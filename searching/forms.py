from django.core.exceptions import ValidationError
from django.forms           import ModelForm

from .models                import Search

#from .views         import tModelFields

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )

class AddOrUpdateForm(ModelForm):
    '''
    using a form to get extra validation
    '''

    def clean(self):
        #
        cleaned = super( AddOrUpdateForm, self).clean()
        #
        cKeyWords       = cleaned.get( 'cKeyWords',     '' )
        iDummyCategory  = cleaned.get( 'iDummyCategory', 0 )
        
        if not ( cKeyWords or iDummyCategory ):
            sMsg = 'key words or ebay category required (having both is OK)'
            raise ValidationError( sMsg, code='invalid' )
        
        return cleaned


    class Meta:
        model   = Search
        fields  = tModelFields