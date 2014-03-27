# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch

from .models import User

# Create your tests here.

class UserTests(TestCase):
    def test_creation(self):
        pass
    
    def test_update(self):
        pass
    
    def test_deletion(self):
        pass
    
    def test_username_generation(self):
        user = User()
        user.preferred_name = u'Toto'
        self.assertEqual(user.guess_username(), u'toto')
        user.preferred_name = u'TotO Tete'
        self.assertEqual(user.guess_username(), u'toto')
        self.assertEqual(user.guess_username(123), u'toto123')
        user.preferred_name = u'Tété#'
        self.assertEqual(user.guess_username(), u'tete')
        
    def test_password_change(self):
        pass