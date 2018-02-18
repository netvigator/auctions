from django.conf.urls import url

from . import views


app_name = "models"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.ModelIndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.ModelDetailView.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.ModelUpdateView.as_view(),
        name    = 'edit' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.ModelDeleteView.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^add/$',
        view    = views.ModelCreateView.as_view(),
        name    = 'add'  ),
    
]
'''

'''