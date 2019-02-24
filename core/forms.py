from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm

from core.validators        import gotTextOutsideParens

from crispy_forms.helper    import FormHelper
from crispy_forms.layout    import Submit

from .mixins                import FindUserMixin


class BaseModelFormGotCrispy( FindUserMixin, ModelForm ):
    #
    '''base crispy form, can subclass to create or update'''
    #

    def __init__( self, *args, **kwargs ):
        #
        self.request = kwargs.get( 'request' )
        # Voila, now you can access request via self.request!
        #
        if 'user' in kwargs:
            #
            self.user = kwargs.pop( 'user' ) # super crashes if kwarg includes
            #
        elif not hasattr( self, 'user' ) or self.user is None:
            #
            self.user = self.findUser( **kwargs )
            #
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
        # oUser = self.FindUserMixin()
        #
        if ( self.Meta.model.objects.filter(
                iUser           = self.user,
                cTitle__exact   = cTitle ).exists() ):
            #
            # using case sensitive here
            # because sometimesyou want to
            # change the capitalization.
            #
            sGotTitle = (
                    'Title "%s" already exists. '
                    '(Putting some info in parens can overcome this glitch.)' )
            #
            oInvalid = ValidationError(
                    sGotTitle % cTitle,
                    code = 'title already exists' )
            #
            self.add_error( 'cTitle', oInvalid )
            #
            #raise oInvalid
        #
        if ( self.Meta.model.objects.filter(
                iUser               = self.user,
                cLookFor__icontains = cTitle ).exists() ):
            #
            oInvalid = ValidationError('Title "%s" is in Look For' % cTitle,
                        code = 'title exists in Look For' )
            #
            self.add_error( 'cLookFor', oInvalid )
            #
            #raise oInvalid
            #

    def clean(self):
        #
        cleaned         = super( ModelFormValidatesTitle, self ).clean()
        #
        bCreating       = ( self.which == 'Create' )
        #
        bEditing        = not bCreating
        #
        # does the title already exist?
        #
        cTitle          = cleaned.get( 'cTitle'   )
        cLookFor        = cleaned.get( 'cLookFor' )
        #
        if cTitle: # cTitle can be None if field invalid
            #
            if bEditing and ( self.instance.cTitle in cLookFor and
                              cTitle in self.instance.cLookFor ):
                #
                pass # just rearranged, no need to query database
                #
            else:
                #
                if bCreating or self.instance.cTitle != cTitle:
                    #
                    self.gotTitleAready( cTitle )
                    #
                #
            #
        #
        return cleaned
