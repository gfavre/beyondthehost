from django.db import models

from model_utils.models import TimeStampedModel

from webfaction.models import OwnedModel


class EmailAddress(TimeStampedModel, OwnedModel):
    address = models.EmailField(max_length=254)
    redirect_to = models.ManyToManyField('Redirect', blank=True, null=True)
    save_to = models.ManyToManyField('Mailbox', blank=True, null=True)
    
class Redirect(TimeStampedModel, OwnedModel):
    address = models.EmailField(max_length=254)

class Mailbox(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=255)
    wf_name = models.CharField(max_length=255)
    enable_spam_protection = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('owner', 'name')

    
    # do something with password
