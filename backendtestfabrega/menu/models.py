from django.db import models
from django.urls import reverse
# Create your models here.


class Menu(models.Model):

    date = models.DateField(unique=True)

    def __str__(self):
        return self.date

    def get_absolute_url(self):
        return reverse('menu:menu_detail', kwargs={'pk': self.pk})

class Meal(models.Model):

    content = models.TextField(null=False, blank=False)

    menu = models.ForeignKey('Menu', null=False, blank=False,
                            on_delete=models.CASCADE, related_name='meals')

    def __str__(self):
        return self.content