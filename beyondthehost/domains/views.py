from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .models import Domain, SubDomain

class DomainActionMixin(object):
    fields = ('name', )
    
    @property
    def success_msg(self):
        return NotImplemented
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(DomainActionMixin, self).form_valid(form)
    
class OwnedMixin(object):
    def get_queryset(self):
        base_qs = super(OwnedMixin, self).get_queryset()
        return base_qs.filter(owner=self.request.user)


class DomainsListView(LoginRequiredMixin, OwnedMixin, ListView):
    model = Domain
    
    def get_queryset(self):
        return self.model.objects.prefetch_related('subdomains')


class DomainsCreateView(LoginRequiredMixin, DomainActionMixin, OwnedMixin, CreateView):
    model = Domain
    success_msg = 'Domain created'
    
class DomainsUpdateView(LoginRequiredMixin, DomainActionMixin, OwnedMixin, UpdateView):
    model = Domain
    success_msg = 'Domain updated'
    
class DomainsDetailView(OwnedMixin, DetailView):
    model = Domain