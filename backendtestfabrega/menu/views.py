from datetime import date
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Menu, Meal 
from .forms import MenuForm, MenuMealFormset
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms




# Create your views here.

class HomeView(TemplateView):
    template_name = 'menu/home.html'

class MenuListView(ListView):
    model = Menu
    template_name = 'menu/menu_list.html'

    def get_queryset(self):
        return Menu.objects.filter(
            date__gte= date.today()
        ).order_by('date')

class MenuCreateView(CreateView):
    form_class = MenuForm
    model = Menu
    template_name = 'menu/menu_create.html'

    

    def form_valid(self, form):
        return super().form_valid(form)
        '''
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The menu was added.'
        )
'''
        

class MenuDetailView(DetailView):
    model = Menu
    template_name = 'menu/menu_detail.html'

class MenuMealsUpdateView(SingleObjectMixin, FormView):

    model = Menu
    template_name = 'menu/menu_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Menu.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Menu.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return MenuMealFormset(
            **self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        '''

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )
        '''

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('menu:menu_detail', kwargs={'pk': self.object.pk})
    


