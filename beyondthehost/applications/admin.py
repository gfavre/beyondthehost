from django.contrib import admin
from .models import Application, Database


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'wf_name', 'owner', )
    list_filter = ('owner',)
    ordering = ('owner__full_name', 'name')
    

admin.site.register(Application, ApplicationAdmin)

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'app')
    list_filter = ('owner',)
    ordering = ('owner__full_name', 'name')
    

admin.site.register(Database, DatabaseAdmin)

