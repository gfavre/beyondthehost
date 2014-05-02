from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from braces.views import LoginRequiredMixin

from .models import Domain, SubDomain

class DomainsListView(LoginRequiredMixin, ListView):
    model = Domain
    
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


