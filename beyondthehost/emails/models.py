from django.db import models

from model_utils.models import TimeStampedModel

class EmailAddress(TimeStampedModel):
    address = models.EmailField(max_length=254)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    redirect_to = models.ManyToManyField('Redirect', blank=True, null=True)
    save_to = models.ManyToManyField('MailBox', blank=True, null=True)
    
class Redirect(TimeStampedModel):
    address = models.EmailField(max_length=254)

class MailBox(TimeStampedModel):
    name = models.CharField(max_length=255)
    enable_spam_protection = models.BooleanField(default=False)
    domain = models.ForeignKey('Domain', related_name='subdomains')
    
    # do something with password
