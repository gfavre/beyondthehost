from django.conf.urls import patterns, include, url

from .views import DomainsListView, DomainsUpdateView

urlpatterns = patterns('',
    url(r'^$', DomainsListView.as_view()),
    url(r'^new$', DomainsListView.as_view()),
    url(r'^(?P<pk>[\d]+)/$', DomainsUpdateView.as_view(), name="domain-detail"),
    url(r'^$', DomainsListView.as_view()),

)

