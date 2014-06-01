from django.contrib import admin
from .models import Application, Database


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    list_filter = ('owner',)
    ordering = ('owner__full_name', 'name')
    

admin.site.register(Application, ApplicationAdmin)


admin.site.register(Database)

