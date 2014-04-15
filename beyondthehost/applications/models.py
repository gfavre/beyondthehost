from django.db import models

from model_utils.models import TimeStampedModel
from model_utils import Choices


from webfaction.models import OwnedModel

class Application(OwnedModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('owner', 'name')
    
class StaticApp(Application):
    apptype = 'static_php54'

class WordPress(Application):
    apptype = 'wordpress_380'
    initial_password = models.CharField(max_length=255, blank=True)

class ManagedApp(Application):
    apptype = 'custom_app_with_port'
    port = models.PositiveIntegerField(null=True, blank=True)


class Database(OwnedModel):
    ENGINES = Choices('mysql', 'postresql')
    
    name = models.CharField(max_length=255, unique=True)
    engine = models.CharField(choices=ENGINES, max_length=15)
    
    class Meta:
        ordering = ('owner', 'name')