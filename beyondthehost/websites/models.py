from django.db import models

from model_utils.models import TimeStampedModel
from model_utils import FieldTracker

from webfaction.models import OwnedModel

class Website(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=250, blank=False)
    domain = models.ManyToManyField('domains.SubDomain', related_name='websites')
    application = models.ForeignKey('applications.Application', related_name='websites')
    
