from django.conf.urls import url

from . import views


app_name = "finders"

urlpatterns = [
    # maybe not used any more, can delete?
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
    url( # if above, this regex will intercept the hit url !
        regex = r'(?P<select>[ADPZ]){0,1}/{0,1}$',
        view    = views.FindersIndexView.as_view(),
        name    = 'index' ),

]

