from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from model_utils import Choices


from webfaction.models import OwnedModel

APPTYPES = Choices(('static_php54', _('Static / PHP / MySQL')), 
                   ('wordpress_380', _('Wordpress')),
                   ('custom_app_with_port', _('Custom')),)
ENGINES = Choices('mysql', 'postgresql')

class Application(OwnedModel, TimeStampedModel):
    
    name = models.CharField(max_length=255)
    wf_name = AutoSlugField(max_length=255, unique=True,
                            populate_from=lambda instance: '%s_%s' % (instance.owner, instance.name),
                            sep='_')
    apptype = models.CharField(choices=APPTYPES, default=APPTYPES.static_php54,
                               blank=False, null=False, max_length=64,
                               verbose_name=_("Application type"))
    
    port = models.PositiveIntegerField(null=True, blank=True)
    extra = models.CharField(max_length=255, blank=True)
    
    
    class Meta:
        ordering = ('owner', 'name')
        unique_together = ('name', 'owner')
    
    @property
    def needed_db_engine(self):
        if self.apptype in ('static_php54', 'wordpress_380'):
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
    
    
    
    # def save...
    # slug version of name
    # to be checked by task if name clashes. perhaps prepend username
    
#class StaticApp(Application):
#    apptype = 'static_php54'
#
#class WordPress(Application):
#    apptype = 'wordpress_380'
#    initial_password = models.CharField(max_length=255, blank=True)
#    
#    
#
#class ManagedApp(Application):
#    apptype = 'custom_app_with_port'
#    port = models.PositiveIntegerField(null=True, blank=True)


class Database(OwnedModel):
    
    name = models.CharField(max_length=255, unique=True)
    engine = models.CharField(choices=ENGINES, max_length=15)
    
    app = models.ForeignKey('applications.Application', null=True)
    
    def guess_db_name(self):
        return slugify('%s-%s' % (self.owner.wf_username, self.app.wf_name))
    
    class Meta:
        ordering = ('owner', 'name')