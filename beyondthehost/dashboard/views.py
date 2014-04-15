# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.template.defaultfilters import filesizeformat

from braces.views import LoginRequiredMixin

from webfaction.utils import WebFactionClient 
#from emails.models import MailBox
from applications.models import Database, Application

    


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        def addsize(alist):
            count = 0
            for element in alist:
                count += int(element.get('size'))
            return count
    
    
        context = super(DashboardView, self).get_context_data(**kwargs)
        #mailboxes = request.user.mailbox_set.all()
        
        databases = {name: engine for (name, engine) in self.request.user.database_set.values_list('name', 'engine')}
        mailboxes = {wf_name: name for (name, wf_name) in self.request.user.mailbox_set.values_list('name', 'wf_name')}

        applications = self.request.user.application_set.values_list('name', flat=True)
        
        wf = WebFactionClient()
        usage_dict = wf.list_disk_usage()
        context['db'] = [(db['name'], db['size'] * 1024) for db in usage_dict['mysql_databases'] if db['name'] in databases]
        context['db'].extend([(db['name'], db['size'] * 1024) for db in usage_dict['postgresql_databases'] if db['name'] in databases])
        
        context['email'] = ([(mailboxes[mailbox['name']], mailbox['size'] * 1024) for mailbox in usage_dict['mailboxes'] if mailbox['name'] in mailboxes])
        home = [home['size'] * 1024 for home in usage_dict['home_directories'] if home['name'] == self.request.user.wf_username][0]

        
        context['quota'] = 1024 * 1024 * 1024 * 100
        app_sizes = wf.system('$HOME/bin/appsize %s' % ' '.join(applications))
        
        context['apps'] = [(app.split(' ')[1], app.split(' ')[0]) for app in app_sizes.split('\n') ]
        
        context['usage'] = addsize(context['email']) + addsize(context['db']) + \
                           addsize(context['apps']) + home
        
        xdata = ['Emails', 'Databases', 'Applications', 'Home folder', 'Free']
        ydata = [addsize(context['email']), addsize(context['db']), addsize(context['apps']), home, context['quota'] - context['usage']]
        
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
        
        
        chartdata = {'x': xdata, 'y': [y/(1024*1024) for y in ydata], 'extra': extra_serie }
        charttype = "pieChart"
        chartcontainer = 'disk_usage'
        context['disk_usage'] = {
            'charttype': charttype,
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