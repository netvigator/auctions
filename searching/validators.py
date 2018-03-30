from django.core.exceptions import ValidationError


def isPriorityValid( sPriority ):
    #
    ''' get whether the priority string is 2 chars long
    1st char uppper alpha
    2nd char digit (or alpha)
    A1 ... Z9'''
    #
    if len( sPriority ) != 2:
        #
        raise ValidationError( 'need 2 charaters, 1st should be alpha' )
        #
    #
    if not sPriority[0].isalpha() :
        #
        raise ValidationError( '1st charater should be alpha' )
        #
    #
    if sPriority.isalnum() or sPriority.isalpha():
        #
        pass # OK
        #
    else:
        #
        raise ValidationError( '2nd charater should be digit (alpha is OK)' )
        #

