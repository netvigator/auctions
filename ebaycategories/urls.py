from django.conf.urls import url

from . import views



app_name = "ebaycategories"

urlpatterns = [
    url(r'^$', views.show_ebay_categories,  name='marketindex'),
    ]