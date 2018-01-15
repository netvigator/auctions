from django.shortcuts   import render

#from django.shortcuts   import render_to_response
#from django.template    import RequestContext

from .models            import EbayCategory

from markets.models     import Market

# Create your views here.

def show_ebay_categories(request, sMarket):
    iMarket = Market.objects.get( cMarket = sMarket.upper() )
    context = { 'eb_categories':EbayCategory.objects.filter(
        iMarket = iMarket, iTreeVersion = iMarket.iCategoryVer ) }
    #context = { 'eb_categories':EbayCategory.objects.all() }
    return render(request, 'ebaycategories/ebay_categories.html', context)


def show_ebay_tree(request, sMarket):
    iMarket = Market.objects.get( cMarket = sMarket.upper() )
    context = { 'eb_categories':EbayCategory.objects.filter(
        iMarket = iMarket, iTreeVersion = iMarket.iCategoryVer ) }
    #context = { 'eb_categories':EbayCategory.objects.all() }
    return render(request, 'ebaycategories/drill_down_tree.html', context)

