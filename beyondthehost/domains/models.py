from django.db import models
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel
from model_utils import FieldTracker

from webfaction.models import OwnedModel
from .tasks import create_domain, delete_domain, delete_subdomain

class Domain(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=253)
    tracker = FieldTracker()
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        "Also creates domain on webfaction"
        super(Domain, self).save(*args, **kwargs)
        if not self.pk:
            return
        create_domain.delay(self.name)
        
        if self.tracker.has_changed('name') and self.tracker.previous('name'):
            delete_domain.delay(self.tracker.previous('name'))  

    def delete(self, *args, **kwargs):
        "Also delete domain on webfaction"
        delete_domain.delay(self.name)
        super(Domain, self).delete(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('domain-detail', kwargs={'pk': self.pk})
    
        
class SubDomain(TimeStampedModel):
    name = models.CharField(max_length=250, blank=True)
    domain = models.ForeignKey('Domain', related_name='subdomains')
    tracker = FieldTracker()

    def __unicode__(self):
        if self.name:
            return '%s.%s' % (self.name, self.domain.name)
        return self.domain.name

    def save(self, *args, **kwargs):
        "Also creates domain on webfaction"
        super(SubDomain, self).save(*args, **kwargs)
        if not self.pk:
            return
        create_domain.delay(self.domain.name)
        
        if self.tracker.has_changed('name') and self.tracker.previous('name'):
            delete_subdomain.delay(self.domain.name, self.tracker.previous('name'))  

    def delete(self, *args, **kwargs):
        "Also delete domain on webfaction"
        delete_subdomain.delay(self.domain.name, self.name)
