
from django.core.exceptions import ValidationError




def require_digits_only( value ):
    #
    '''
    Value is OK if digits only, raise a ValidationError if not
    '''
    #
    if not isinstance( value, int ):
        sMsg = 'Only digits are valid!'
        raise ValidationError( sMsg )


