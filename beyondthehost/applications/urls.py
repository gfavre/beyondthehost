from django.conf.urls import patterns, include, url

from .views import ListApplicationsView, CreateApplicationView, UpdateApplicationView, DeleteApplicationView

urlpatterns = patterns('',
    url(r'^$', ListApplicationsView.as_view(), name="applications-list"),
    url(r'^new/$', CreateApplicationView.as_view(), name="applications-create"),
    url(r'^(?P<pk>[\d]+)/$', UpdateApplicationView.as_view(), name="applications-detail"),
    url(r'^(?P<pk>[\d]+)/delete/$', DeleteApplicationView.as_view(), name="applications-delete"),


)

