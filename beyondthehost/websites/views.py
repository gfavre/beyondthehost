from django.shortcuts import render_to_response
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView


from applications.forms import AppForm
from domains.forms import DomainSelectForm
from .forms import URLForm

def show_create_domain(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('paytype') or {'method': 'none'}


class WebsiteWizard(NamedUrlSessionWizardView):
    template_name = 'website/wizard/wizard_form.html'
    form_list = [('app', AppForm), ('url', URLForm), ('domain', DomainSelectForm)]
    condition_dict = {}
    
    def done(self, form_list, **kwargs):
        return render_to_response('website/wizard/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    
    def get_form_kwargs(self, step):
        kwargs = super(WebsiteWizard, self).get_form_kwargs()
        if step == 'domain':
            kwargs['user'] = self.request.user
        return kwargs



# Create your views here.
