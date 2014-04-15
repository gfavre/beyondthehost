# -*- coding: utf-8 -*-
from django.test import TestCase

#from mock import patch
import mock
from .models import User

# Create your tests here.


class UserTests(TestCase):
    @mock.patch('webfaction.tasks.create_user.delay')
    def test_creation(self, create_user_task):
        preferred_name = u'Brian'        
        user1 = User(email=u'brian@alwayslook.com', 
                     preferred_name=preferred_name)
        user1.save()
        create_user_task.assert_called_once_with(user1.pk, 
                                                 user1.guess_username(), 
                                                 'none')
        
        shell = 'tcsh'
        user2 = User(email=u'brian@onthebright.org', 
                     preferred_name=preferred_name, 
                     shell=shell)
        user2.save()
        create_user_task.assert_called_with(user2.pk, 
                                            user2.guess_username(), 
                                            shell)
            
    @mock.patch('webfaction.tasks.delete_user.delay')        
    @mock.patch('webfaction.tasks.create_user.delay')
    def test_update(self, create_user_task, delete_user_task):
        preferred_name = u'Brian'
        user1 = User(email=u'brian@alwayslook.com', 
                     preferred_name=preferred_name)
        user1.save()
        wf_username = user1.guess_username()
        user1.wf_username = wf_username
        user1.save()
        self.assertEqual(create_user_task.call_count, 1) 
        
        user1.full_name = 'Brian Cohen'
        user1.save()
        self.assertEqual(create_user_task.call_count, 1)
        
        user1.wf_username = user1.guess_username('1234')
        user1.save()
        delete_user_task.assert_called_with(wf_username)
        create_user_task.assert_called_with(user1.pk, 
                                            user1.guess_username('1234'), 
                                            'none')


    @mock.patch('webfaction.tasks.delete_user.delay')            
    @mock.patch('webfaction.tasks.create_user.delay')    
    def test_deletion(self, create_user_task, delete_user_task):
        preferred_name = u'Brian'
        user1 = User(email=u'brian@alwayslook.com', 
                     preferred_name=preferred_name)
        user1.save()
        user1.delete()
        self.assertEqual(delete_user_task.call_count, 0)
        
        user2 = User(email=u'brian@alwayslook.com', 
                     preferred_name=preferred_name)
        wf_username = user2.guess_username()
        user2.wf_username = wf_username
        user2.save()
        user2.delete()
        delete_user_task.assert_called_with(wf_username)
    
    def test_username_generation(self):
        user = User()
        user.preferred_name = u'Brian'
        self.assertEqual(user.guess_username(), u'brian')
        user.preferred_name = u'Brian Cohen'
        self.assertEqual(user.guess_username(), u'brian')
        self.assertEqual(user.guess_username(123), u'brian123')
        user.preferred_name = u'Têté'
        self.assertEqual(user.guess_username(), u'tete')

    @mock.patch('webfaction.tasks.change_user_password.delay')
    @mock.patch('webfaction.tasks.create_user.delay')           
    def test_password_change(self, create_user_task, 
                                   change_user_password_task):
        preferred_name = u'Arthur'        
        user = User(email=u'king@brittons.net', 
                     preferred_name=preferred_name)
        user.set_password('ni')
        self.assertEqual(change_user_password_task.call_count, 0)
        user.wf_username = user.guess_username()
        user.set_password('it')
        change_user_password_task.assert_called_with(user.wf_username, 'it')

