from django.shortcuts   import render

from .models            import EbayCategory

# Create your views here.

def show_ebay_categories(request):
    return render_to_response("ebay_categories.html",
        {'nodes':EbayCategory.objects.all()},
        context_instance=RequestContext(request))