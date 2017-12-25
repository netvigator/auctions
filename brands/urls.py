from django.conf.urls import url

from . import views



app_name = "brands"

urlpatterns = [
    url(r'^$',      views.IndexView.as_view(),  name='index'),
    url(r'^add$',   views.BrandCreate.as_view(),name='add'),  # works
    url(r'^(?P<pk>[0-9]+)/$',
                    views.BrandDetail.as_view(),name='detail'),
    url(r'^(?P<pk>[0-9]+)/delete/$',
                    views.BrandDelete.as_view(),name='delete'),
    url(r'^(?P<pk>[0-9]+)/edit/$',
                    views.BrandUpdate.as_view(),name='edit'),
    
]

'''    
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new$', views.CreateBrandView.as_view(),
        name='brands-new',),
'''