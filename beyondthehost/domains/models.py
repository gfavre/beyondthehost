from django.db import models

from model_utils.models import TimeStampedModel

from webfaction.models import OwnedModel


class Domain(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=253)
    
    def __unicode__(self):
        return self.name
    
        
class SubDomain(TimeStampedModel):
    name = models.CharField(max_length=250)
    domain = models.ForeignKey('Domain', related_name='subdomains', blank=True)
    
    def __unicode__(self):
        if self.name:
            return '%s.%s' % (self.name, self.domain.name)
        return self.domain.name

