from django.conf.urls import url

from . import views



app_name = "searching"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.SearchIndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^add/$', # SearchViewSuccessPostFormValidMixin references
        view    = views.SearchCreateView.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.SearchDetailView.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.SearchDeleteView.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.SearchUpdateView.as_view(),
        name    = 'edit' ),
]

'''

'''
