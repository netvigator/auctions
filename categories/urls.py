from django.conf.urls import url

from . import views


app_name = "categories"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.IndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.CategoryDetail.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.CategoryUpdate.as_view(),
        name    = 'edit' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.CategoryDelete.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^add$',
        view    = views.CategoryCreate.as_view(),
        name    = 'add'  ),
    
]
'''

'''