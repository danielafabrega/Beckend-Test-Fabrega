from django.urls import path, include

from . import views


app_name = 'users'

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/choice/', views.createChoiceView, name='choice'),
    path('users/afterlogin', views.afterLogin, name='afterlogin'),
    #path('users/logout/', views.logout, name='logout')
    ]