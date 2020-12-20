from django.urls import path

from . import views


app_name = 'menu'

urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuListView.as_view(), name='menu_list'),
    path('menu/add/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menu/<uuid:pk>/detail',views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/<uuid:pk>/meals/edit/', views.MenuMealsUpdateView.as_view(),name='meal_update'),
    path('menu/<uuid:pk>/',views.MenuDailyView.as_view(), name='menu_daily'),
    path('menu/<uuid:pk>/select_meal',views.selectMealView, name='select_meal'),
]