from django.conf.urls import url

from . import views



app_name = "models"
'''
urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.IndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^add$',
        view    = views.ModelCreate.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.ModelDetail.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.ModelDelete.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.ModelUpdate.as_view(),
        name    = 'edit' ),
    
]

'''