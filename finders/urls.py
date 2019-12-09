from django.conf.urls import url

from . import views


#        view    = views.ItemsFoundIndexView.as_view(),
#        view    = views.FindersIndexView.as_view(),


app_name = "finders"

urlpatterns = [
    url( # this one needs to be above the index url !!!!
        regex   = r'^hit/(?P<pk>[0-9]+)/$',
        view    = views.ItemFoundHitView.as_view(),
        name    = 'hit' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.ItemFoundDetailView.as_view(),
        name    = 'detail' ),
    url(
        regex   = r'(?P<pk>[0-9]+)/edit/$',
        view    = views.ItemFoundUpdateView.as_view(),
        name    = 'edit' ),
    url(
        regex = r'(?P<select>[ADPZ]){0,1}/{0,1}$',
        view    = views.FindersIndexView.as_view(),
        name    = 'index' ),

]

