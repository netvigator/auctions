from django.forms       import ModelForm

from core.crispy        import FormHelper
from core.dj_import     import ValidationError
from core.validators    import gotTextOutsideParens


class BaseModelFormGotCrispy( ModelForm ):
    #
    '''base crispy form, can subclass to create or update'''
    #

    def __init__( self, *args, **kwargs ):
        #
        self.request = kwargs.get( 'request' )
        # Voila, now you can access request via self.request!
        #
        self.user = None
        #
        if 'user' in kwargs:
            #
            self.user = kwargs.pop( 'user' ) # super crashes if kwarg includes
            #
        elif self.request:
            #
            self.user = self.request.user
            #
        elif 'iUser' in kwargs:
            #
            self.user = kwargs.pop( 'iUser' )
            #
        elif hasattr( self, 'user' ) and self.user:
            #
            self.user = self.user
            #
        elif ( hasattr( self, 'instance' ) and
               hasattr( self.instance, 'user' ) and
               self.instance.user ):
            #
            self.user = self.instance.user
            #
        elif ( hasattr( self, 'instance' ) and
               hasattr( self.instance, 'iUser' ) and
               self.instance.iUser ): # testing
            #
            self.user = self.instance.iUser
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
    #
    def __init__( self, *args, **kwargs ):
        #
        self.bCreating = kwargs.get( 'instance' ) is None
        #
        super( ModelFormValidatesTitle, self ).__init__( *args, **kwargs )
        #
        self.fields[ 'cTitle' ].validators.append( gotTextOutsideParens )
        #

    def gotTitleAready( self, cTitle ):
        #
        sFieldName = self.Meta.model._meta.get_field('cTitle').verbose_name
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
                    '%s %s already exists. '
                    '(Putting some info in parens can overcome this glitch.)'
                     % ( sFieldName, cTitle ) )
            #
            oInvalid = ValidationError(
                    sGotTitle,
                    code = 'title already exists' )
            #
            self.add_error( 'cTitle', oInvalid )
            #
            #raise oInvalid
            #
        #
        if ( self.Meta.model.objects.filter(
                iUser               = self.user,
                cLookFor__icontains = cTitle ).exists() ):
            #
            oGot = self.Meta.model.objects.filter(
                iUser               = self.user,
                cLookFor__icontains  = cTitle )[ 0 ]
            #
            oInvalid = ValidationError(
                    'Cannot put %s in %s, '
                    '%s is already in Look_For for %s %s' %
                    ( cTitle, sFieldName, cTitle, sFieldName, oGot.cTitle ),
                    code = 'title exists in Look_For' )
            #
            self.add_error( 'cLookFor', oInvalid )
            #
            #raise oInvalid
            #

    def clean(self):
        #
        '''on edit, usually check whether title is already in database
        tested in categories/test_forms'''
        #
        cleaned         = super( ModelFormValidatesTitle, self ).clean()
        #
        bCreating       = self.bCreating
        #
        bEditing        = not bCreating
        #
        # does the title already exist?
        #
        cTitle          = cleaned.get( 'cTitle'   )
        cLookFor        = cleaned.get( 'cLookFor' )
        #
        if not cTitle: return cleaned # cTitle can be None if field invalid
        #
        #
        if bEditing and ( self.instance.cLookFor           and
                          self.instance.cTitle in cLookFor and
                          cTitle in self.instance.cLookFor ):
            #
            pass # just rearranged, no need to query database
            #
        elif bCreating or self.instance.cTitle != cTitle:
            #
            self.gotTitleAready( cTitle )
            #
        #
        #
        return cleaned
