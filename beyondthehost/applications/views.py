from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView


from braces.views import LoginRequiredMixin

from beyondthehost.models import OwnedMixin
from .forms import ApplicationForm
from .models import Application, Database


class ListApplicationsView(LoginRequiredMixin, OwnedMixin, ListView):
    model = Application

class CreateApplicationView(LoginRequiredMixin, OwnedMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()

        self.populate_wf_app_name()
        self.create_database()  
        self.populate_extra_field()
        return super(CreateApplicationView, self).form_valid(form)
    
    def populate_wf_app_name(self):
        pass
    
    def create_database(self):
        engine = self.object.needed_db_engine
        if engine:
            db = Database(owner=self.request.user, 
                          engine=engine, 
                          app=self.object)
            db.name = db.guess_db_name
    
    def populate_extra_field(self):
        pass

class DetailApplicationView(LoginRequiredMixin, OwnedMixin, DetailView):
    model = Application

class DeleteApplicationView(LoginRequiredMixin, OwnedMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('applications-list')
