from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from model_utils import Choices


from webfaction.models import OwnedModel

APPTYPES = Choices(('static', _("HTML website")),
                   ('phpmysql', _('PHP / MySQL')), 
                   ('wordpress', _('Wordpress')),
                   ('custom', _('Custom')),)

ENGINES = Choices('mysql', 'postgresql')

TYPE_TO_WF = {'static': 'static_only',
              'phpmysql': 'static_php55',
              'wordpress': 'wordpress_380',
              'custom': 'custom_app_with_port'
              }

class Application(OwnedModel, TimeStampedModel):
    
    name = models.CharField(max_length=255)
    wf_name = AutoSlugField(max_length=255, unique=True,
                            populate_from=lambda instance: '%s_%s' % (instance.owner.wf_username, instance.name),
                            sep='_')
    apptype = models.CharField(choices=APPTYPES, default=APPTYPES.static,
                               blank=False, null=False, max_length=64,
                               verbose_name=_("Application type"))
    
    port = models.PositiveIntegerField(null=True, blank=True)
    extra = models.CharField(max_length=255, blank=True)
    
    
    class Meta:
        ordering = ('owner', 'name')
        unique_together = ('name', 'owner')
    
    @property
    def needed_db_engine(self):
        if self.apptype in ('phpmysql', 'wordpress'):
            return ENGINES.mysql
        return None
    
    def needs_db(self):
        return self.needed_db_engine != None
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, APPTYPES[self.apptype])
    
    def get_absolute_url(self):
        return reverse('applications-detail', kwargs={'pk': self.pk})
 
    def get_delete_url(self):
        return reverse('applications-delete', kwargs={'pk': self.pk})
    


class Database(OwnedModel):
    
    name = AutoSlugField(populate_from=lambda instance: instance.app.wf_name)
    engine = models.CharField(choices=ENGINES, max_length=15)
    
    app = models.ForeignKey('applications.Application', null=True)
        
    class Meta:
        ordering = ('owner', 'name')
    
    def __unicode__(self):
        return self.name