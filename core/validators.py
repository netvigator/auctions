from django.core.exceptions import ValidationError

from core.utils             import oInParensFinder

from String.Eat             import eatFromWithin

def gotTextOutsideParens( sTitle ):
    #
    '''
    title is required and can have text in parens
    but something should be outside parens
    having only text within parens is no good
    raise ValidationError if everything is in parens
    '''
    #
    sWhatsLeft = eatFromWithin( sTitle, oInParensFinder ).strip()
    #
    if not sWhatsLeft: raise ValidationError