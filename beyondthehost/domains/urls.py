from django.conf.urls import patterns, include, url

from .views import DomainsListView

urlpatterns = patterns('',
    url(r'^$', DomainsListView.as_view()),
)

