from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm

from core.validators        import gotTextOutsideParens


class ModelFormValidatesTitle( ModelForm ):
    #
    which = 'Create' # can be over written in view get_form
    #
    def __init__( self, *args, **kwargs ):
        #
        if 'user' in kwargs: self.user = kwargs.pop('user')
        #
        super( ModelFormValidatesTitle, self ).__init__( *args, **kwargs )
        #
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        #

    def gotTitleAready( self, cTitle ):
        #
        oUser = None
        #
        if hasattr( self, 'user' ):
            oUser = self.user
        elif hasattr( self, 'request' ):
            oUser = self.request.user
        elif hasattr( self.instance, 'user' ):
            oUser = self.instance.user
        elif hasattr( self.instance, 'iUser' ): # testing
            oUser = self.instance.iUser
        #
        if ( self.Meta.model.objects.filter(
                iUser           = oUser ).filter(
                cTitle__iexact  = cTitle ).exists() ):
            #
            raise ValidationError('Title "%s" already exists' % cTitle,
                        code = 'title already exists' )
        #
        if ( self.Meta.model.objects.filter(
                iUser               = oUser ).filter(
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
        if cTitle and doCheckTitle: # cTitle can be None if field invalid
            #
            self.gotTitleAready( cTitle )
            #
        #
