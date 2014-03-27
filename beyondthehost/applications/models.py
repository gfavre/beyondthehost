from django.db import models

from model_utils.models import TimeStampedModel

class BaseApp(models.Model)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
    
class StaticApp(BaseApp, TimeStampedModel):
    apptype = 'static_php54'

class WordPress(BaseApp, TimeStampedModel):
    apptype = 'wordpress_380'
    initial_password = models.CharField(max_length=255, blank=True)

class ManagedApp(BaseApp, TimeStampedModel):
    apptype = 'custom_app_with_port'
    port = models.PositiveIntegerField(null=True, blank=True)