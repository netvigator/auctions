from django.forms       import ModelForm, ChoiceField

from core.crispy        import FormHelper, Field, Layout, Submit
from core.dj_import     import ValidationError
from core.validators    import gotTextOutsideParens

from models.models      import Model

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

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
        super().__init__( *args, **kwargs )
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
        super().__init__( *args, **kwargs )
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
        if any( self.errors ):
            # Don't bother validating the formset unless each form is valid on its own
            return
        #
        cleaned         = super().clean()
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


class BaseUserFinderKeeperFormGotCrispy( BaseModelFormGotCrispy ):
    #
    '''using a form on the edit user item found or keeper page'''
    #
    gModel = ChoiceField(
                    label='Generic Models '
                          '(more than one brand may offer this model)' )


    def __init__( self, *args, **kwargs ):
        #
        super().__init__( *args, **kwargs )
        #
        '''
        if False and 'iItemNumb_id' in kwargs:
            #
            print( kwargs['iItemNumb_id'] )
            self.fields['iItemNumb_id'] = kwargs['iItemNumb_id']
            #
        else:
            if 'request' in self.__dict__:
                print( 'self.request:', self.request )
            print( 'args:', args )
            print( 'kwargs:', kwargs )
            if 'args' in self.__dict__:
                print( 'self.args:', self.args )
            if 'kwargs' in self.__dict__:
                print( 'self.kwargs:', self.kwargs )
        '''
        #
        if self.instance.iBrand:
            self.fields["iModel"].queryset = (
                    Model.objects.filter(
                            iUser  = self.user,
                            iBrand = self.instance.iBrand ) )
        else:
            self.fields["iModel"].queryset = Model.objects.filter(
                                              iUser = self.user )
        #
        #
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        #
        self.fields['gModel'].choices = (
                ( o.pk, o.cTitle )
                  for o in Model.objects.filter(
                            iUser  = self.user,
                            bGenericModel = True) )
        #
        self.fields['gModel'].required = False
        #
        # model could be None
        if self.instance.iModel and self.instance.iModel.bGenericModel:
            #
            self.fields['gModel'].initial = self.instance.iModel_id
            #
        #
        self.helper.layout = Layout(
                'iModel',
                'gModel',
                'iBrand',
                'iCategory',
                'bGetResult',
                Field( 'iHitStars', readonly = True ), )

    def clean( self ):
        #
        if any( self.errors ):
            # Don't bother validating the formset unless each form is valid on its own
            return
        #
        cleaned = super().clean()
        #
        igModel = self.cleaned_data['gModel']
        iModel  = self.cleaned_data['iModel']
        #
        if igModel and not iModel:
            #
            self.cleaned_data['iModel'] = Model.objects.get( pk = igModel )
            #
        #
        return cleaned
