from django.shortcuts   import render

from django.shortcuts   import render_to_response
from django.template    import RequestContext

from .models            import EbayCategory

# Create your views here.

def show_ebay_categories(request):
    context = {'nodes':EbayCategory.objects.all()}
    return render(request, 'ebaycategories/ebay_categories.html', context)