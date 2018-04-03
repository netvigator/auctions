from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm

from core.validators        import gotTextOutsideParens

from crispy_forms.helper    import FormHelper
from crispy_forms.layout    import Submit



class BaseModelFormGotCrispy( ModelForm ):
    #
    '''base crispy form, can subclass to create or update'''
    #
    def __init__( self, *args, **kwargs ):
        #
        self.request = kwargs.get( 'request' )
        # Voila, now you can access request via self.request!
        #
        if not hasattr( self, 'user' ): self.user = None
        #
        if 'user' in kwargs: self.user = kwargs.pop('user')
        #
        super( BaseModelFormGotCrispy, self ).__init__( *args, **kwargs )
        #
        self.helper = FormHelper()
        #
        #
        # subclass should set:
        # self.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        # or
        # self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        # and
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
    


class ModelFormValidatesTitle( BaseModelFormGotCrispy ):
    #
    which = 'Create' # can be over written
    #
    def __init__( self, *args, **kwargs ):
        #
        super( ModelFormValidatesTitle, self ).__init__( *args, **kwargs )
        #
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        #

    def gotTitleAready( self, cTitle ):
        #
        # oUser = None
        #
        #
        if hasattr( self, 'user' ) and self.user is not None:
            oUser = self.user
        elif ( hasattr( self, 'request' ) and
               hasattr( self.request, 'user' ) and
               self.request.user is not None ):
            oUser = self.request.user
        elif ( hasattr( self.instance, 'user' ) and
               self.instance.user is not None ):
            oUser = self.instance.user
        elif ( hasattr( self.instance, 'iUser' ) and
               self.instance.iUser is not None ): # testing
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
