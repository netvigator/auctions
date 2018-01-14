from django.conf.urls import url

from . import views



app_name = "searching"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.IndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^add$',
        view    = views.SearchCreate.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.SearchDetail.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.SearchDelete.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.SearchUpdate.as_view(),
        name    = 'edit' ),
    
]

'''

'''