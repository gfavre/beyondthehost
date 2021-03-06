# -*- coding: utf-8 -*-
"User model, connected with webfaction"
from django.db import models
from django.utils.text import slugify
from django.conf import settings

from authtools.models import AbstractEmailUser
from model_utils import Choices, FieldTracker

from .tasks import create_user, delete_user, change_user_password

class Server(models.Model):
    name = models.CharField(max_length=255, blank=False)
    ip_address = models.GenericIPAddressField(blank=False)
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.ip_address)
    


class User(AbstractEmailUser):
    "User, connected with Webfaction shell users"
    SHELLS = Choices('none', 'bash', 'sh', 'ksh', 'csh', 'tcsh')
    
    full_name = models.CharField('full name', max_length=255, blank=False)
    preferred_name = models.CharField('preferred name', max_length=255, blank=False)
    wf_username = models.CharField('Webfaction username', max_length=12, blank=True, null=True)
    shell = models.CharField(choices=SHELLS, blank=True, 
                             default=SHELLS.none, max_length=15)
    server = models.ForeignKey('Server', related_name='users', null=True)

    REQUIRED_FIELDS = ('full_name', )
    tracker = FieldTracker()
    
    def get_full_name(self):
        "Get name of user"
        return self.full_name

    def get_short_name(self):
        "Nickname of user"
        return self.preferred_name
    
    def guess_username(self, added_char=None):
        "Username to be used on Webfaction SSH/FTP login"
        if not added_char:
            added_char = u''
        return u'%s%s' % (slugify(self.get_short_name()).split(u'-')[0],
                          added_char)
    
    def save(self, *args, **kwargs):
        "Also creates user on webfaction"
        super(User, self).save(*args, **kwargs)
        if not self.pk:
            return
        if not self.wf_username:
            create_user.delay(self.pk, self.guess_username(), self.shell)
        elif self.tracker.has_changed('wf_username') and \
             self.tracker.previous('wf_username'):
            create_user.delay(self.pk, self.wf_username, self.shell)
            delete_user.delay(self.tracker.previous('wf_username'))  
    
    
    def delete(self, *args, **kwargs):
        "Also delete user on webfaction"
        if self.wf_username:
            delete_user.delay(self.wf_username)
        super(User, self).delete(*args, **kwargs)
        
    def set_password(self, raw_password):
        "Synchronize password with Webfaction"
        super(User, self).set_password(raw_password)
        if self.wf_username:
            change_user_password.delay(self.wf_username, raw_password)
        

class OwnedModel(models.Model):
    "A model defining an owner relationship"
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    
    class Meta:
        abstract = True