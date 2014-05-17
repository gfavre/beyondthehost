from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from extra_views import InlineFormSet, InlineFormSetView, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet

from braces.views import LoginRequiredMixin

from beyondthehost.models import OwnedMixin

from .forms import DomainForm, SubDomainForm, HorizontalNoFormHelper, InlineSubDomainHelper
from .models import Domain, SubDomain

class DomainActionMixin(object):
    fields = ('name', )
    
    @property
    def success_msg(self):
        return NotImplemented
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(DomainActionMixin, self).form_valid(form)
    

class SubDomainsInline(InlineFormSet):
    model = SubDomain
    extra = 1
        
class CrispyHelperMixin(object):
    def get_context_data(self, **kwargs):
         context = super(CrispyHelperMixin, self).get_context_data(**kwargs)
         context['helper'] = InlineSubDomainHelper()
         return context


class ListDomainsView(LoginRequiredMixin, OwnedMixin, ListView):
    model = Domain
    
    def get_queryset(self):
        return self.model.objects.prefetch_related('subdomains')


class CreateDomainView(LoginRequiredMixin, DomainActionMixin, OwnedMixin, CrispyHelperMixin, 
                       CreateWithInlinesView):
    model = Domain
    form_class = DomainForm
    inlines = [SubDomainsInline, ]
    success_msg = 'Domain created'
    
    def get_success_url(self):
        return self.object.get_absolute_url()
        
    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())        
    
    
class UpdateDomainView(LoginRequiredMixin, DomainActionMixin, OwnedMixin, CrispyHelperMixin, 
                       UpdateWithInlinesView):
    model = Domain
    form_class = DomainForm
    can_delete = True

    inlines = [SubDomainsInline, ]
    success_msg = 'Domain updated'

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteDomainView(LoginRequiredMixin, OwnedMixin, DeleteView):
    model = Domain
    success_url = reverse_lazy('domains-list')