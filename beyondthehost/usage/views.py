# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.template.defaultfilters import filesizeformat

from braces.views import LoginRequiredMixin

from webfaction.utils import WebFactionClient 
#from emails.models import MailBox
from applications.models import Database, Application
from webfaction.utils import WebFactionClient 

from .utils import disk_usage, megabytes

QUOTA = 1024 * 1024 * 1024 * 100

class WebFactionMixin:
    def __init__(self, *args, **kwargs):
        self.wf_client = WebFactionClient()
    


class DiskGraphView(LoginRequiredMixin, WebFactionMixin, View):
    def __init__(self, *args, **kwargs):
        super(DiskGraphView, self).__init__(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        def addsize(alist):
            count = 0
            for element in alist:
                count += element.get('size')
            return count
        
        context = super(DiskGraphView, self).get_context_data(**kwargs)
        
        usage_dict = disk_usage(self.request.user, self.wf_client)
        context.update(usage_dict)
        context['quota'] = QUOTA
        context['usage'] = addsize(context['email']) + addsize(context['db']) + \
                           addsize(context['apps']) + context['home']
        context['usage_percent'] = int(100.0 * context['usage'] / context['quota'])
        
        xdata = ['Emails', 'Databases', 'Applications', 'Home folder', 'Free']
        ydata = [addsize(context['email']), 
                 addsize(context['db']), 
                 addsize(context['apps']), 
                 context['home'], 
                 context['quota'] - context['usage']]
        
        color_list = ('#5d8aa8', # emails
                      '#e32636', # databases
                      '#efdecd', # applications
                      '#ffbf00', # home
                      'lightgray', # free
        )

        extra_serie = {
        "tooltip": {"y_start": "", "y_end": " MiB"},
        "color_list": color_list,
        }
        
        chartdata = {'x': xdata, 'y': [megabytes(y) for y in ydata], 'extra': extra_serie }
        context['disk_usage'] = {
            'charttype': 'pieChart',
            'chartdata': chartdata,
            'chartcontainer': 'disk_usage',
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return context
        


class DiskUsageView(DiskGraphView, TemplateView):
    template_name = 'usage/disk.html'
    
    def add_app_breakdown(self, context):
        xdata = [app.get('name') for app in context['apps']]
        ydata = [app.get('size') for app in context['apps']]
        
        extra_serie = {
        "tooltip": {"y_start": "", "y_end": " MiB"},
        }
        
        chartdata = {'x': xdata, 'y': [megabytes(y) for y in ydata], 'extra': extra_serie }
        context['app_breakdown'] = {
            'charttype': 'pieChart',
            'chartdata': chartdata,
            'chartcontainer': 'app_breakdown',
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        }
        return context


class BandwidthUsageView(LoginRequiredMixin, WebFactionMixin, TemplateView):        
    template_name = 'usage/bandwidth.html'
    

""""
from webfaction.models import User

from webfaction.utils import WebFactionClient 
from applications.models import Database, Application, StaticApp, ManagedApp, WordPress
from emails.models import Mailbox

w = WebFactionClient()
usage_dict = w.list_disk_usage()

user= User.objects.get(id=1)


databases = {name: engine for (name, engine) in user.database_set.values_list('name', 'engine')}
mailboxes = {wf_name: name for (name, wf_name) in user.mailbox_set.values_list('name', 'wf_name')}
applications = user.application_set.values_list('name', flat=True)

#db = Database(name='grfavre_mariage', engine='postgresql', owner=user)
#db.save()
#db = Database(name='grfavre_phytotm', engine='postgresql', owner=user)
#db.save()
#db = Database(name='dealguru', engine='postgresql', owner=user)
#db.save()
#db = Database(name='beyondthewall', engine='postgresql', owner=user)
#db.save()
#db = Database(name='sportfac', engine='postgresql', owner=user)
#db.save()

usage = {}
usage['db'] = [(db['name'], db['size']) for db in usage_dict['mysql_databases'] if db['name'] in databases]
usage['db'].append([(db['name'], db['size']) for db in usage_dict['postgresql_databases'] if db['name'] in databases])

#Mailbox.objects.create(name='grfavre', wf_name='grfavre', owner=user)
#Mailbox.objects.create(name='affiliate', wf_name='grfavre_affiliate', owner=user)
#Mailbox.objects.create(name='community', wf_name='grfavre_community', owner=user)
#Mailbox.objects.create(name='katia', wf_name='grfavre_katia', owner=user)
#Mailbox.objects.create(name='kyanh', wf_name='grfavre_kyanh', owner=user)
#Mailbox.objects.create(name='mariage', wf_name='grfavre_mariage', owner=user)
#Mailbox.objects.create(name='phytotm', wf_name='grfavre_phytotm', owner=user)

type_to_class = {'custom_app_with_port': ManagedApp, 
                 'static_only': StaticApp,
                 'static_php54': StaticApp,
                 'wordpress_381': WordPress,
                 'node-0.10.24': ManagedApp,
                 'git': ManagedApp,}
#for app in w.list_apps():
#    type_to_class[app['type']].objects.create(name=app['name'], owner=user)





"""