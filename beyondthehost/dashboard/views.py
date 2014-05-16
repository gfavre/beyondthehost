# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.template.defaultfilters import filesizeformat

from braces.views import LoginRequiredMixin


from webfaction.utils import WebFactionClient 
#from emails.models import MailBox
from applications.models import Database, Application

from usage.views import DiskGraphView
    


class DashboardView(DiskGraphView, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        def addsize(alist):
            count = 0
            for element in alist:
                count += int(element.get('size'))
            return count
        
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['domains'] = self.request.user.domain_set.all()
        context['websites'] = self.request.user.website_set.all()        

        
        return context