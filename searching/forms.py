from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.db              import IntegrityError
from django.forms           import ModelForm

from .models                import Search

from ebaycategories.models  import EbayCategory

#from .views         import tModelFields

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )

class SearchAddOrUpdateForm(ModelForm):
    '''
    using a form to get extra validation
    '''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get( 'request' )
        # Voila, now you can access request via self.request!
        super(SearchAddOrUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        #
        cleaned = super( SearchAddOrUpdateForm, self).clean()
        #
        cKeyWords       = cleaned.get( 'cKeyWords',     '' )
        
        iDummyCategory  = cleaned.get( 'iDummyCategory', None )
        iDummyOriginal  = self.instance.iDummyCategory

        if iDummyOriginal and not iDummyCategory:
            sMsg = 'Your ebay category "%s" is invalid' % iDummyOriginal
            raise ValidationError( sMsg, code='invalid ebay category' )
            
        if not ( cKeyWords or iDummyCategory ):
            sMsg = 'key words or ebay category required (having both is OK)'
            raise ValidationError( sMsg, code='invalid' )
        
        if iDummyCategory is not None:
            #
            try:
                iEbayCategory = EbayCategory.objects.get(
                    iMarket_id = self.request.user.iMarket,
                    iCategoryID = iDummyCategory )
            except ObjectDoesNotExist:
                sMsg = '"%s" not an ebay category number!'
                raise ValidationError( sMsg,
                        params = ( iDummyCategory ),
                        code='ebay category number not found' )
            #
            cleaned['iEbayCategory'] = iEbayCategory
            #
        #
        cPriority           = cleaned.get( 'cPriority' )
        #
        bCreating = ( self.which == 'Create' )
        #
        doCheckPriority = bCreating or self.instance.cPriority != cPriority
        #
        if doCheckPriority and (
            Search.objects.filter(
                iUser       = self.request.user,
                cPriority   = cPriority ).exists() ):
            #
            raise ValidationError('Priority "%s" already exists' % cPriority,
                        code='cPriority already exists' )
        #
        cTitle              = cleaned.get( 'cTitle' )
        #
        doCheckTitle = bCreating or self.instance.cTitle != cTitle
        #
        if doCheckTitle and (
            Search.objects.filter(
                iUser           = self.request.user ).filter(
                cTitle__iexact  = cTitle ).exists() ):
            #
            raise ValidationError('Title "%s" already exists' % cTitle,
                        code='title already exists' )
        #
        cKeyWords           = cleaned.get( 'cKeyWords'      )
        iEbayCategory       = cleaned.get( 'iEbayCategory'  )
        #
        doCheckSearch = (   bCreating or
                            self.instance.cKeyWords != cKeyWords or
                            self.instance.iEbayCategory != iEbayCategory )
        if doCheckSearch and (
            Search.objects.filter(
                iUser               = self.request.user,
                iEbayCategory       = iEbayCategory ).filter(
                cKeyWords__iexact   = cKeyWords ).exists() ):
            #
            # really need to compare sets
            #
            raise ValidationError(
                'You are already searching for "%s" in "%s"!' %
                ( cKeyWords, iEbayCategory.name ),
                        code='already searching for keywords in ebay category' )
        #
        return cleaned

    class Meta:
        model   = Search
        fields  = tModelFields