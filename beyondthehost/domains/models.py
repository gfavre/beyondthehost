from django.db import models

from model_utils.models import TimeStampedModel

class Domain(TimeStampedModel):
    name = models.CharField(max_length=253)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    
class SubDomain(TimeStampedModel):
    name = models.CharField(max_length=250)
    domain = models.ForeignKey('Domain', related_name='subdomains')


