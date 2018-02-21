from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms           import ModelForm

from .models                import Search, ItemFound

from ebayinfo.models        import EbayCategory


tSearchFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )

class SearchAddOrUpdateForm(ModelForm):
    '''
    using a form to get extra validation
    '''
    which = 'Create' # can be over written in view get_form
    #

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get( 'request' )
        # Voila, now you can access request via self.request!
        #
        if 'which' in kwargs:
            self.which = kwargs.pop('which')
        #
        super().__init__(*args, **kwargs)
        # SearchAddOrUpdateForm, self

    def clean(self):
        #
        cleaned = super( SearchAddOrUpdateForm, self).clean()
        #
        sKeyWords       = cleaned.get( 'cKeyWords',     '' )
        
        iDummyCategory  = cleaned.get( 'iDummyCategory', None )
        iDummyOriginal  = self.instance.iDummyCategory

        if iDummyOriginal and not iDummyCategory:
            sMsg = 'Your ebay category "%s" is invalid' % iDummyOriginal
            raise ValidationError( sMsg, code='invalid ebay category' )
            
        if not ( sKeyWords or iDummyCategory ):
            sMsg = 'key words or ebay category required (having both is OK)'
            raise ValidationError( sMsg, code='invalid' )
        
        #print( 'iDummyCategory:', iDummyCategory )
        #print( 'iDummyOriginal:', iDummyOriginal )
        #
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
        #print( "cleaned['iEbayCategory']:", cleaned['iEbayCategory'] )
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
        #
        doCheckSearch = (   bCreating or
                            self.instance.cKeyWords != sKeyWords or
                            self.instance.iEbayCategory != iEbayCategory )
        #
        if doCheckSearch:
            #
            sKeyWords           = cleaned.get( 'cKeyWords'      )
            iEbayCategory       = cleaned.get( 'iEbayCategory'  )
            #
            if iEbayCategory:
                #
                if Search.objects.filter(
                        iUser               = self.request.user,
                        iEbayCategory       = iEbayCategory ).filter(
                        cKeyWords__iexact   = sKeyWords ).exists():
                    #
                    oEbayCategory = EbayCategory.get( iCategoryID = iEbayCategory )
                    #
                    raise ValidationError(
                        'You are already searching for "%s" in "%s"!' %
                        ( sKeyWords, oEbayCategory.name ),
                                code='already searching for keywords in ebay category' )
                #
            else:
                #
                if Search.objects.filter(
                        iUser     = self.request.user ).filter(
                        cKeyWords__iexact = sKeyWords ).exists():
                    #
                    raise ValidationError(
                        'You are already searching for "%s"!' % sKeyWords,
                                code='already searching for same keywords' )
                #
            #
            # really need to compare sets
            #
        #
        return cleaned

    class Meta:
        model   = Search
        fields  = tSearchFields


tItemFoundFields = (
    'iItemNumb',
    'cTitle',
    'cLocation',
    'cCountry',
    'cMarket',
    'cGalleryURL',
    'cEbayItemURL',
    'tTimeBeg',
    'tTimeEnd',
    'bBestOfferable',
    'bBuyItNowable',
    'cListingType',
    'lLocalCurrency',
    'lCurrentPrice',
    'dCurrentPrice',
    'iCategoryID',
    'cCategory',
    'iConditionID',
    'cCondition',
    'cSellingState' )

class ItemFoundForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model   = ItemFound
        fields  = tItemFoundFields



