import datetime
from django.test import TestCase
from .models import Menu, Meal, Choice
from django.urls import reverse
from django.contrib.auth.models import User, Permission



# Create your tests here.

def create_menu(date):
    return Menu.objects.create(date=date)

def create_meal(content, menu):
    return Meal.objects.create(content=content, menu=menu)

def create_choice(meal, user):
    choice = Choice()
    choice.meal = meal
    choice.user = user
    choice.date = choice.meal.menu.date
    choice.note = "without salt"
    choice.save()
    return choice

class MenuListViewTests(TestCase):
    
    def test_cant_access_menu_list(self):
    #A guest user cannot enter the list to create menus
        response = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/login?next=/menu/")
    
    def test_employee_access_meal_select(self):
    #An employee can enter to choose their food
        menu = create_menu(date=datetime.datetime.now())
        self.user_2 = User.objects.create_user('John Smith', 'thedoctor@cornershop.com', 'badwolf')
        self.client.login(username='John Smith', password='badwolf')
        response = self.client.get(reverse('menu:select_meal',  kwargs={'pk': menu.id}))
        self.assertEqual(response.status_code, 200)

    def test_can_access_menu_without_login(self):
        #anyone can see the daily menu
        menu = create_menu(date=datetime.datetime.now())
        response = self.client.get(reverse('menu:menu_daily', kwargs={'pk': menu.id}))
        self.assertEqual(response.status_code, 200)

    def test_nora_access_menu_create(self):
        #Nora can create a menu
        self.user = User.objects.create_user('Nora', 'nora@nora.com', 'norapass')
        permission = Permission.objects.get(name='Is nora')
        self.user.user_permissions.add(permission)
        self.client.login(username='Nora', password='norapass')
        response = self.client.get(reverse('menu:menu_create'))
        self.assertEqual(response.status_code, 200)

class ModelChoiceTest(TestCase):
    #test that only one meal can be selected per employee
    def test_only_one_choice(self):
        menu = create_menu(date=datetime.datetime.now())
        meal_1 = create_meal("chicken with salad", menu)
        meal_2 = create_meal("tuna salad", menu)
        user = User.objects.create_user('John Smith', 'thedoctor@cornershop.com', 'badwolf')
        self.client.login(username='John Smith', password='badwolf')
        #No choice
        self.assertEqual(len(Choice.objects.all()), 0)
        create_choice(meal_1, user)
        #First choice
        self.assertEqual(len(Choice.objects.all()), 1)
        create_choice(meal_2, user)
        #Try to choose again
        self.assertEqual(len(Choice.objects.all()), 1)





    


        
    

    
