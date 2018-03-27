from django.shortcuts   import render

#from django.shortcuts   import render_to_response
#from django.template    import RequestContext

from .models            import EbayCategory, Market

# Create your views here but keep them thin.

def show_ebay_categories(request, sMarket):
    oMarket = Market.objects.get( cMarket = sMarket.upper() )
    context = { 'eb_categories':EbayCategory.objects.filter(
        iEbaySiteID = oMarket, iTreeVersion = oMarket.iCategoryVer ) }
    #context = { 'eb_categories':EbayCategory.objects.all() }
    return render(request, 'ebaycategories/ebay_categories.html', context)


def show_ebay_tree(request, sMarket):
    oMarket = Market.objects.get( cMarket = sMarket.upper() )
    context = { 'eb_categories':EbayCategory.objects.filter(
        iEbaySiteID = oMarket, iTreeVersion = oMarket.iCategoryVer ) }
    #context = { 'eb_categories':EbayCategory.objects.all() }
    return render(request, 'ebaycategories/drill_down_tree.html', context)

