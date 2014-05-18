# -*- coding: utf-8 -*-
from webfaction.utils import WebFactionClient 

def bytes(kb):
    return kb * 1024

def megabytes(bytes):
    return bytes / (1024 * 1024)


def disk_usage(user, wf_client=None):
    if wf_client is None:
        wf_client = WebFactionClient()

    databases = {name: engine for (name, engine) in user.database_set.values_list('name', 'engine')}
    mailboxes = {wf_name: name for (name, wf_name) in user.mailbox_set.values_list('name', 'wf_name')}
    applications = user.application_set.values_list('name', flat=True)

    usage_dict = wf_client.list_disk_usage()
    
    mysql = [{'name': db['name'], 'size': bytes(db['size']), 'engine': 'MySQL'} for \
             db in usage_dict['mysql_databases'] if db['name'] in databases]
    postgres = [{'name': db['name'], 'size': bytes(db['size']), 'engine': 'PostgreSQL'} for \
                 db in usage_dict['postgresql_databases'] if db['name'] in databases]
    db = mysql + postgres
    
    email = [{'name': mailboxes[mailbox['name']], 'size': bytes(mailbox['size'])} for \
             mailbox in usage_dict['mailboxes'] if mailbox['name'] in mailboxes]
    
    if user.wf_username:
        home = [bytes(home['size']) for home in usage_dict['home_directories'] if home['name'] == user.wf_username][0]
    else:
        home = 0
    
    app_sizes = wf_client.system('$HOME/bin/appsize %s' % ' '.join(applications))
    apps = [{'name': app.split(' ')[1], 'size': int(app.split(' ')[0])} for app in app_sizes.split('\n') ]
    
    return {'db': db, 'email': email, 'home': home, 'apps': apps}
    
def bandwidth_usage(user, wf_client=None):
    if wf_client is None:
        wf_client = WebFactionClient()
    
    websites = {name: engine for (name, engine) in user.database_set.values_list('name', 'engine')}


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