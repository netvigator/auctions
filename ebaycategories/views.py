from django.shortcuts   import render

from django.shortcuts   import render_to_response
from django.template    import RequestContext

from .models            import EbayCategory

from markets.models     import Market
# Create your views here.

def show_ebay_categories(request, sMarket):
    iMarket = Market.objects.get( cMarket = sMarket.upper() )
    context = { 'nodes':EbayCategory.objects.filter(
        iMarket = iMarket, iTreeVersion = iMarket.iCategoryVer ) }
    return render(request, 'ebaycategories/ebay_categories.html', context)