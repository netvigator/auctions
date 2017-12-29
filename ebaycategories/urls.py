from django.conf.urls import url

from . import views



app_name = "ebaycategories"

urlpatterns = [
    (r'^ebay_categories/$', views.show_ebay_categories,  name='index'),
    ]