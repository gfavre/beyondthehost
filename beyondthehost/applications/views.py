from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.utils.translation import ugettext as _


from braces.views import LoginRequiredMixin

from beyondthehost.models import OwnedMixin
from beyondthehost.views import MessageMixin

from .forms import ApplicationForm
from .models import Application, Database


class ListApplicationsView(LoginRequiredMixin, OwnedMixin, ListView):
    model = Application

class CreateApplicationView(LoginRequiredMixin, MessageMixin, OwnedMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    success_msg = _('Application created')

    
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        self.create_database()  
        self.populate_extra_field()
        return super(CreateApplicationView, self).form_valid(form)
        
    def create_database(self):
        engine = self.object.needed_db_engine
        if engine:
            db = Database.objects.create(
                    owner=self.request.user, 
                    engine=engine, 
                    app=self.object)
    
    def populate_extra_field(self):
        pass

class DetailApplicationView(LoginRequiredMixin, OwnedMixin, DetailView):
    model = Application

class DeleteApplicationView(LoginRequiredMixin, MessageMixin, OwnedMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('applications-list')
    success_msg = _('Application deleted')

