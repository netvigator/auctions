from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm

from core.validators        import gotTextOutsideParens


class ModelFormValidatesTitle( ModelForm ):
    #
    def __init__( self, *args, **kwargs ):
        #
        super( ModelFormValidatesTitle, self ).__init__( *args, **kwargs )
        #
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
    '''
    problem in clean():
    AttributeError: 'BrandForm' object has no attribute 'which'
    
    def gotTitleAready( self, cTitle ):
        #
        if ( model.objects.filter(
                iUser           = self.request.user ).filter(
                cTitle__iexact  = cTitle ).exists() ):
            #
            raise ValidationError('Title "%s" already exists' % cTitle,
                        code = 'title already exists' )
        #
        if ( Search.objects.filter(
                iUser               = self.request.user ).filter(
                cLookFor__icontains = cTitle ).exists() ):
            #
            raise ValidationError('Title "%s" is in Look For' % cTitle,
                        code = 'title exists in Look For' )

    def clean(self):
        #
        cleaned     = super( ModelFormValidatesTitle, self ).clean()
        #
        bCreating   = ( self.which == 'Create' )
        #
        # does the title already exist?
        #
        cTitle      = cleaned.get( 'cTitle' )
        #
        doCheckTitle = bCreating or self.instance.cTitle != cTitle
        #
        if doCheckTitle:
            #
            self.gotTitleAready( cTitle )
            #
        #
       ''' 
