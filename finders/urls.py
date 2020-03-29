from django.conf.urls import url

from . import views


app_name = "finders"

urlpatterns = [
    # maybe not used any more, can delete?
    # hit view is one user item found
    # there could be other brands or models for the item
    # (other hits should be listed)
    url( # specific ones need to be above the index url !!!!
        regex   = r'^hit/(?P<pk>[0-9]+)/$',
        view    = views.ItemFoundHitView.as_view(),
        name    = 'hit' ),
    url(
        regex   = r'^add/$',
        view    = views.ItemFoundCreateView.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.ItemFoundDetailView.as_view(),
        name    = 'detail' ),
    url(
        # can edit one user item found --
        # change brand, model or caregory for the item
        regex   = r'edit/(?P<pk>[0-9]+)/$',
        view    = views.ItemFoundUpdateView.as_view(),
        name    = 'edit' ),
    url( # keep this url at bottom, this regex will intercept the hit url !
        regex = r'(?P<select>[ADS]){0,1}/{0,1}$',
        view    = views.FinderIndexView.as_view(),
        name    = 'index' ),

]

