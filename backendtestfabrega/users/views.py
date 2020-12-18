from django.shortcuts import render


# Create your views here.
def PruebaView(request):
    
   return render(request, "users/prueba.html")