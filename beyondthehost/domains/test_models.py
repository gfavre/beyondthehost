# -*- coding: utf-8 -*-
from django.test import TestCase

import mock

from webfaction.models import User
from .models import Domain, SubDomain


class DomainTests(TestCase):
    
    def setUp(self):
        with mock.patch('webfaction.tasks.create_user.delay'):
            self.owner = User.objects.create(email=u'brian@alwayslook.com', 
                                             preferred_name=u'Brian')
            self.domain_name = 'flying-circus.com'

    @mock.patch('domains.tasks.create_domain.delay')
    def test_creation(self, create_domain_task):
        Domain.objects.create(name=self.domain_name, owner=self.owner)
        create_domain_task.assert_called_once_with(self.domain_name)

    @mock.patch('domains.tasks.delete_domain.delay')            
    @mock.patch('domains.tasks.create_domain.delay')        
    def test_update(self, create_domain_task, delete_domain_task):
        new_name = 'holy-grail.com'

        domain = Domain.objects.create(name=self.domain_name, owner=self.owner)        
        domain.name = new_name
        domain.save()
        self.assertEqual(create_domain_task.call_count, 2)
        create_domain_task.assert_called_with(new_name)
        delete_domain_task.assert_called_with(self.domain_name)

    @mock.patch('domains.tasks.delete_domain.delay')
    def test_deletion(self, delete_domain_task):
        with mock.patch('domains.tasks.create_domain.delay'):
            domain = Domain.objects.create(name=self.domain_name, owner=self.owner)
        domain.delete()
        delete_domain_task.assert_called_once_with(self.domain_name)


class SubDomainTests(TestCase):
    
    def setUp(self):
        with mock.patch('webfaction.tasks.create_user.delay'):
            self.owner = User.objects.create(email=u'brian@alwayslook.com', 
                                             preferred_name=u'Brian')
        with mock.patch('domains.tasks.create_domain.delay'):
            self.domain = Domain.objects.create(name='flying-circus.com', 
                                                owner=self.owner) 
    @mock.patch('domains.tasks.create_domain.delay')
    def test_creation(self, create_domain_task):
        name = 'flying-circus.com'
        subdomain = SubDomain.objects.create(name='www', domain=self.domain)
        create_domain_task.assert_called_once_with(name)
    
    @mock.patch('domains.tasks.delete_subdomain.delay')            
    @mock.patch('domains.tasks.create_domain.delay')        
    def test_update(self, create_domain_task, delete_subdomain_task):
        initial_sub = 'www'
        new_sub = 'monty'
        subdomain = SubDomain.objects.create(name=initial_sub, domain=self.domain)
        subdomain.name = new_sub
        subdomain.save()
        self.assertEqual(create_domain_task.call_count, 2)
        create_domain_task.assert_called_with(self.domain.name)
        delete_subdomain_task.assert_called_with(self.domain.name, initial_sub)
    
    @mock.patch('domains.tasks.delete_subdomain.delay')            
    def test_deletion(self, delete_subdomain_task):
        name = 'www'
        with mock.patch('domains.tasks.create_domain.delay'):
            subdomain = SubDomain.objects.create(name=name, domain=self.domain)
        subdomain.delete()
        delete_subdomain_task.assert_called_with(self.domain.name, name)
