from django.conf.urls import url

from . import views



app_name = "finders"

urlpatterns = [
    url(
        regex   = r'(?P<pk>[0-9]+)/edit/$',
        view    = views.ItemFoundUpdateView.as_view(),
        name    = 'edit' ),
    url(
        regex   = r'(?P<select>[ADPZadpz]){0,1}/{0,1}$', # testing cannot
        view    = views.ItemsFoundIndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'(?P<pk>[0-9]+)/*$',
        view    = views.ItemFoundDetailView.as_view(),
        name    = 'detail' ),

]

