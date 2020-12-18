from django.urls import path, include

from . import views


app_name = 'users'

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/prueba/', views.PruebaView, name='prueba')
    ]