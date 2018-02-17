from django.conf.urls import url

from . import views


app_name = "categories"

urlpatterns = [
    url(
        regex   = r'^$',
        view    = views.CategoryIndexView.as_view(),
        name    = 'index' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/$',
        view    = views.CategoryDetailView.as_view(),
        name    = 'detail'),
    url(
        regex   = r'^(?P<pk>[0-9]+)/edit/$',
        view    = views.CategoryUpdateView.as_view(),
        name    = 'edit' ),
    url(
        regex   = r'^(?P<pk>[0-9]+)/delete/$',
        view    = views.CategoryDeleteView.as_view(),
        name    = 'delete'),
    url(
        regex   = r'^add$',
        view    = views.CategoryCreateView.as_view(),
        name    = 'add'  ),
    
]
'''

'''