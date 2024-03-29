from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from django.views import defaults as default_views

from .views import CollectionsListView, UserVisitView

urlpatterns = [
    url(r'^$', CollectionsListView.as_view(
                template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(
                template_name='pages/about.html'), name='about'),
    url(r'^visiting/(?P<pk>[0-9]+)/$', UserVisitView.as_view(
                template_name='users/visiting.html'), name='visiting'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    url(r'^admin/',     include( 'admin_honeypot.urls','admin_honeypot' ), ),
    # User management
    url(r'^users/',     include(('auctionbot.users.urls', 'users')) ),
    url(r'^accounts/',  include('allauth.urls')),

    # Your stuff: custom urls includes go here

    url(r'^ebayinfo/',  include( 'ebayinfo.urls',    namespace="ebayinfo")),
    url(r'^brands/',    include( 'brands.urls',      namespace="brands")),
    url(r'^models/',    include( 'models.urls',      namespace="models")),
    url(r'^categories/',include( 'categories.urls',  namespace="categories")),
    url(r'^searching/', include( 'searching.urls',   namespace="searching")),
    url(r'^finders/',   include( 'finders.urls',     namespace="finders")),
    url(r'^keepers/',   include( 'keepers.urls',     namespace="keepers")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
                        kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
                        kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
                        kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
