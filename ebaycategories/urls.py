from django.conf.urls import url

from . import views



app_name = "ebaycategories"

urlpatterns = [
    url(
        regex   = r'^(?P<sMarket>EBAY-[A-Z]{2,5})/$',
        view    = views.show_ebay_categories,
        name    = 'marketindex' ),
    ]