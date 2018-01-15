from django.conf.urls import url

from . import views



app_name = "ebaycategories"

urlpatterns = [
    url(
        # regex   = r'^(?P<sMarket>(EBAY|ebay)-[A-Za-z]{2,5})/$',
        regex   = r'^(?P<sMarket>ebay-[a-z]{2,5})/$',
        view    = views.show_ebay_categories,
        name    = 'ebay_categories_index' ),
    url(
        regex   = r'^(?P<sMarket>EBAY-[A-Z]{2,5})/$',
        view    = views.show_ebay_tree,
        name    = 'ebay_categories_tree' ),
    ]
    
