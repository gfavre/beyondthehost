from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin

from dashboard.views import DashboardView



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usage/', include('usage.urls')),
    url(r'^domains/', include('domains.urls')),
    url(r'^applications/', include('applications.urls')),

    url(r'^sites/', include('websites.urls')),
    
    (r'^accounts/', include('registration.backends.default.urls')),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
