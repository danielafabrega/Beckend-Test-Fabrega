from datetime import date
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Menu, Meal 
from .forms import MenuForm, MenuMealFormset
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin




# Create your views here.

class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = 'menu.is_nora'
    template_name = 'menu/home.html'

class MenuListView(PermissionRequiredMixin, ListView):
    permission_required = 'menu.is_nora'
    model = Menu
    template_name = 'menu/menu_list.html'

    def get_queryset(self):
        return Menu.objects.filter(
            date__gte= date.today()
        ).order_by('date')

class MenuCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'menu.is_nora'
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
        

class MenuDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'menu.is_nora'
    model = Menu
    template_name = 'menu/menu_detail.html'



class MenuMealsUpdateView(PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'menu.is_nora'
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
        return reverse('menu:menu_detail',  kwargs={'pk': self.object.pk})
    
class MenuDailyView(DetailView):
    permission_required = 'menu.is_nora'
    model = Menu
    template_name = 'menu/menu_daily.html'


  
def selectMealView(request, pk):
    print(pk)
    
    menu = Menu.objects.get(pk=pk)
    print(menu.date)
    return render(request, "menu/select_meal.html",  {'menu': menu})



    '''   
class ChoiceMealView(DetailView):
    #print(self.request)
    model = Menu
    template_name = 'menu/meal_choice.html'

    #def get(self, request):
    #   return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super(ChoiceMealView, self).get_context_data(**kwargs)
        menu_por_nosotro = Menu.objects.get(pk=self.request.resolver_match.kwargs.get('pk'))
        context['menu_as'] = menu_por_nosotro
        #print(dir(self.request))
        #print(self.request.resolver_match)
        print(self.request.resolver_match.kwargs.get('pk'))
        context['Hola'] = "soy un string que va desde la vista"

        #print(**kwargs['pk'])
        #print(context.keys)
        #context = self.get_context_data(object=self.object)
        



        #print(self.request.META)



        #cart_product_form = CartAddProductForm()
        #context['cart_product_form'] = cart_product_form
        return context
'''



