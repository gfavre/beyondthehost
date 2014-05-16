from django.conf.urls import patterns, include, url

from .views import ListDomainsView, CreateDomainView, UpdateDomainView, DeleteDomainView

urlpatterns = patterns('',
    url(r'^$', ListDomainsView.as_view(), name="domains-list"),
    url(r'^new/$', CreateDomainView.as_view(), name="domains-create"),
    url(r'^(?P<pk>[\d]+)/$', UpdateDomainView.as_view(), name="domains-detail"),
    url(r'^(?P<pk>[\d]+)/delete/$', DeleteDomainView.as_view(), name="domains-delete"),


)

