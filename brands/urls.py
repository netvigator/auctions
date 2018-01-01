from django.conf.urls import url

from . import views



app_name = "brands"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.IndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^add$',
        view    = views.BrandCreate.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.BrandDetail.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.BrandDelete.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.BrandUpdate.as_view(),
        name    = 'edit' ),
    
]

'''    
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new$', views.CreateBrandView.as_view(),
        name='brands-new',),
'''