from django.conf.urls import patterns, include, url

from .views import DiskUsageView

urlpatterns = patterns('',
    url(r'^$', DiskUsageView.as_view()),
    url(r'^disk/', DiskUsageView.as_view(), name='usage-disk'),
    url(r'^bandwidth/', DiskUsageView.as_view(), name='usage-bandwidth'),

)

