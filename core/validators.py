from django.core.exceptions import ValidationError

from core.utils             import getWhatsNotInParens


def gotTextOutsideParens( sTitle ):
    #
    '''
    title is required and can have text in parens
    but something should be outside parens
    having only text within parens is no good
    raise ValidationError if everything is in parens
    '''
    #
    sWhatsLeft = getWhatsNotInParens( sTitle )
    #
    if not sWhatsLeft:
        raise ValidationError(
                'You need some text outside the parens () !!!' )
