
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ebaycategories.models  import EbayCategory


class EbayCategoryFormValidMixin(object):

    def form_valid(self, form):
        #
        form.instance.iUser = self.request.user
        #
        iDummyCategory = form.cleaned_data.get('iDummyCategory', '')
        #
        if iDummyCategory:
            #
            try:
                iEbayCategory = EbayCategory.objects.get(
                    iMarket_id = self.request.user.iMarket, 
                    iCategoryID = iDummyCategory )
            except ObjectDoesNotExist:
                sMsg = '"%s" not an ebay category number)'
                raise ValidationError( sMsg,
                                params = ( iDummyCategory ) )
            #
        form.instance.iEbayCategory = iEbayCategory
        #
        return super().form_valid(form)

