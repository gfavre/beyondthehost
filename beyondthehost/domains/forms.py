from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions

from beyondthehost.forms import HorizontalNoFormHelper
from .models import Domain, SubDomain



class InlineSubDomainHelper(HorizontalNoFormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineSubDomainHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            'name',
            'DELETE'
        )


class DomainSelectForm(forms.Form):
    domains = forms.ModelMultipleChoiceField(queryset=SubDomain.objects.all())
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DomainSelectForm, self).__init__(*args, **kwargs)
        
        self.fields['domains'].queryset = SubDomain.objects.filter(domain__owner=user)
        queryset = SubDomain.objects.filter(domain__owner=user)
        
        helper = FormHelper()
        
        helper.form_class = 'form-horizontal'
        #helper.label_class = 'col-lg-2'
        #helper.field_class = 'col-lg-6'
        helper.layout = Layout(
            'domains',
            FormActions(
                Submit('next', 'Next'),
            ),
        )
        self.helper = helper


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        exclude = ('owner',)
    
    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.helper = HorizontalNoFormHelper()    


class SubDomainForm(forms.ModelForm):
    class Meta:
        model = SubDomain
    
    def __init__(self, *args, **kwargs):
        super(SubDomainForm, self).__init__(*args, **kwargs)
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-6'
        helper.form_tag = False
        helper.disable_csrf = True

        self.helper = helper

