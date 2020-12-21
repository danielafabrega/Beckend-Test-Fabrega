from django.db import models
from django.urls import reverse
import uuid
from django.conf import settings
# Create your models here.


class Menu(models.Model):
    '''
represents the menu entity
    
date field: saves the dates of the menus, 
            it is a unique field since there cannot be two menus on the same date
id: unique identifier to be able to access a particular menu
    '''
    date = models.DateField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.date

    def get_absolute_url(self):
        return reverse('menu:menu_detail', kwargs={'pk': self.pk})

    class Meta:
        #add custom permission
        permissions={
            ('is_nora', 'Is nora')
        }
    
    
class Meal(models.Model):
    '''
represents the meal entity
content: a meal from the menu
menu: a meal is associated with a single menu


    '''
    content = models.TextField(null=False, blank=False)

    menu = models.ForeignKey('Menu', null=False, blank=False,
                            on_delete=models.CASCADE, related_name='meals')

    def __str__(self):
        return self.content

class Choice(models.Model):
    '''
represents an employee choice
note: Text field representing employee specifications about meal
user: link a meal to an employee
date: menu date, included to make a tuple of "user date"

    '''
    meal = models.ForeignKey('Meal', null=True, on_delete=models.CASCADE )
    note = models.TextField(null=True, blank=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date = models.DateField()

    class Meta:
        unique_together = ('date', 'user',)

    def __str__(self):
        return self.user.get_username() +" "+ self.meal.content +" "+'{0.month}/{0.day}/{0.year}'.format(self.date) 

    
    