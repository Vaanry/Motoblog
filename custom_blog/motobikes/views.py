from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Owners
from .models import Motobike
from .forms import MotobikeForm


class CatalogListView(ListView):
    model = Motobike
    ordering = 'name'
    paginate_by = 10
    template_name = 'moto/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        return context
    
    
class MotoDetailView(DetailView):
    model = Motobike
    template_name = 'moto/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.resolver_match.kwargs['pk']
        owners = Owners.objects.values('owner__username').filter(motorbike=pk)
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        context['owners']=[owner['owner__username'] for owner in owners]
        return context


class MotoCreateView(LoginRequiredMixin, CreateView):
    model = Motobike
    template_name = 'moto/create.html'
    form_class = MotobikeForm

    def form_valid(self, form):
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('moto:catalog')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        return context


class EditMotoView(LoginRequiredMixin, UpdateView):
    model = Motobike
    template_name = 'moto/create.html'
    form_class = MotobikeForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse_lazy('moto:moto_detail', kwargs={'pk':
                            pk})
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        return context