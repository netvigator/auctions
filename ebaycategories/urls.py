from django.conf.urls import url

from . import views



app_name = "ebaycategories"

urlpatterns = [
    url(
        regex   = r'^(?P<sMarket>(EBAY|ebay)-[A-Za-z]{2,5})/$',
        view    = views.show_ebay_categories,
        name    = 'marketindex' ),
    ]