from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from beyondthehost.models import OwnedMixin
from .models import Application, Database


class ListApplicationsView(LoginRequiredMixin, OwnedMixin, ListView):
    model = Application

class CreateApplicationView(LoginRequiredMixin, OwnedMixin, CreateView):
    model = Application
    
    def form_valid(self, form):
        self.populate_wf_app_name()
        self.create_database()  
        self.populate_extra_field()
        return super(CreateAppView, self).form_valid(form)
    
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

class UpdateApplicationView(LoginRequiredMixin, OwnedMixin, UpdateView):
    model = Application

class DeleteApplicationView(LoginRequiredMixin, OwnedMixin, DeleteView):
    model = Application
