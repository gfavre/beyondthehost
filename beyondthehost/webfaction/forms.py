from django import forms
from django.utils.translation import ugettext_lazy as _

from authtools.forms import AdminUserChangeForm, UserCreationForm

from .models import User


class WFAdminUserChangeForm(AdminUserChangeForm):
    wf_username = forms.CharField(label=_("Webfaction username"))
    shell = forms.ChoiceField(choices=User.SHELLS)
    
    class Meta:
        model = User    

class WFUserCreationForm(UserCreationForm):
    shell = forms.ChoiceField(choices=User.SHELLS)
    
