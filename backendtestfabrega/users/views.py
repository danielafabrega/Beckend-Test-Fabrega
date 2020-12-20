import datetime
from django.shortcuts import render
from menu.models import Menu, Meal, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def createChoiceView(request):
   meal= Meal.objects.get(pk=request.POST.get("meal"))
   now = datetime.datetime.now()
   time_limit= datetime.datetime.combine(meal.menu.date, datetime.time(11,00,00))
   if (now < time_limit):
   #print(request.POST.get("meal"))
   #print(request.POST)
      choice = Choice()
      choice.meal = meal
      choice.user = request.user
      choice.note = request.POST.get('customizations')
      choice.date = choice.meal.menu.date
      choice.save()
      #print(choice.meal)
      #print(dir(request.user))
      #print(choice.meal.menu.date)
      #print(Meal.objects.get(pk=request.POST.get("meal")))
      #print(choice.meal)
      return render(request, "users/choice.html",  {'meal': choice.meal})
   else:
      return render(request,"users/time_out.html")

def afterLogin(request):
   if request.user.has_perm('menu.is_nora'):
      return HttpResponseRedirect('/')
   else:

      return HttpResponseRedirect(reverse('users:login'))

#def logout(request):
 #  logout(request)
   #return redirect('/')
   #print("hola")