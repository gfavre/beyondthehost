from django.conf.urls import patterns, include, url
from django.core.files.storage import FileSystemStorage

from .views import WebsiteWizard

wizard = WebsiteWizard.as_view(url_name='website-wizard_step', done_step_name='finished')
urlpatterns = patterns('',
    url(r'^wizard/(?P<step>.+)/$', wizard, name='website-wizard_step'),
    url(r'^wizard/$', wizard, name="website-wizard")

)

