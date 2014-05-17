from django.conf.urls import patterns, url

from .views import WebsiteWizard, ListWebsitesView

wizard = WebsiteWizard.as_view(url_name='website-wizard_step', done_step_name='finished')

urlpatterns = patterns('',
    url(r'^$', ListWebsitesView.as_view(), name="website-list"),
    url(r'^wizard/(?P<step>.+)/$', wizard, name='website-wizard_step'),
    url(r'^wizard/$', wizard, name="website-wizard"),
)

