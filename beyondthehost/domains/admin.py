from django.contrib import admin
from .models import Domain, SubDomain


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'subdomains')
    list_filter = ('owner',)
    ordering = ('owner__full_name', 'name')
    
    def subdomains(self, obj):
        return ', '.join([subdomain.name for subdomain in obj.subdomains.all() if subdomain.name])
    

admin.site.register(Domain, DomainAdmin)
admin.site.register(SubDomain)
