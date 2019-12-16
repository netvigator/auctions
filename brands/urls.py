from django.conf.urls import url

from . import views



app_name = "brands"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.BrandIndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^add/$',
        view    = views.BrandCreateView.as_view(),
        name    = 'add'  ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.BrandDetailView.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^delete/(?P<pk>[0-9]+)/$',
        view    = views.BrandDeleteView.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^edit/(?P<pk>[0-9]+)/$',
        view    = views.BrandUpdateView.as_view(),
        name    = 'edit' ),

]

'''
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new$', views.CreateBrandView.as_view(),
        name='brands-new',),
'''
