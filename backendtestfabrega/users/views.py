import datetime
from django.shortcuts import render
from menu.models import Menu, Meal, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def createChoiceView(request):
   '''
   Compare the current time and 11 am, to send a choice only if the current time is 
   less than 11 am.
   
   Each choice has a meal, an employee, a specification and a date
   '''
   meal= Meal.objects.get(pk=request.POST.get("meal"))
   now = datetime.datetime.now()
   time_limit= datetime.datetime.combine(meal.menu.date, datetime.time(11,00,00))
   if (now < time_limit):
      choice = Choice()
      choice.meal = meal
      choice.user = request.user
      choice.note = request.POST.get('customizations')
      choice.date = choice.meal.menu.date
      choice.save()
      return render(request, "users/choice.html",  {'meal': choice.meal})
   else:
      return render(request,"users/time_out.html")

def afterLogin(request):
   #redirects "afterlogin" if you try to enter directly to the url users/login
   if request.user.has_perm('menu.is_nora'):
      return HttpResponseRedirect('/')
   else:

      return HttpResponseRedirect(reverse('users:login'))

