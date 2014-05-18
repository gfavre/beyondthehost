from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from authtools.forms import AdminUserChangeForm, UserCreationForm
from authtools.admin import StrippedUserAdmin, BASE_FIELDS, SIMPLE_PERMISSION_FIELDS

from .models import User, Server
from .forms import WFUserCreationForm, WFAdminUserChangeForm


def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
delete_model.short_description = _('Delete selected users (also from webfaction)')


REQUIRED_FIELDS = (User.USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)

BASE_EDIT_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password',),
})
BASE_ADD_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password1', 'password2'),
})
WEBFACTION_EDIT_FIELDS = (_('Webfaction'), {
                       'fields': ('wf_username', 'shell', 'server')
})
WEBFACTION_ADD_FIELDS = (_('Webfaction'), {
                       'fields': ('shell', 'server')
})


class UserAdmin(StrippedUserAdmin):
    actions = [delete_model]
    form = WFAdminUserChangeForm
    addform = WFUserCreationForm
    
    fieldsets = (BASE_EDIT_FIELDS, WEBFACTION_EDIT_FIELDS, SIMPLE_PERMISSION_FIELDS)
    add_fieldsets = (BASE_ADD_FIELDS, WEBFACTION_ADD_FIELDS)
    
    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    

admin.site.register(User, UserAdmin)
admin.site.register(Server)