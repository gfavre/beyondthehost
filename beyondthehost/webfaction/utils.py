import os, xmlrpclib

from django.conf import settings

class WebFactionClient():
    def __init__(self):
        API_URL = 'https://api.webfaction.com/'
        try:
            http_proxy = os.environ['http_proxy']
        except KeyError:
            http_proxy = None
        self.server = xmlrpclib.Server(API_URL, transport=http_proxy)
        self.session_id, self.account = self.login()
    
    def login(self):
        return self.server.login(settings.WEBFACTION_USER, 
                                 settings.WEBFACTION_PASSWORD)
    
    def __repr__(self):
        return 'Webfaction API client'
    
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return getattr(self.server, name)(self.session_id, *args, **kwargs)
        return _missing