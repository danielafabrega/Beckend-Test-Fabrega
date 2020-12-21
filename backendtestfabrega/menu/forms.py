from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from .models import Menu, Meal


class DateInput(forms.DateInput): 
    input_type = 'date'
    format = 'YYYY-MM-DD'

def current_date(value):
    #Avoid creating a menu in the past
    if date.today() >= value:
        raise ValidationError("you are trying to create a menu in the past")

    

class MenuForm(forms.ModelForm):
    #Create an empty menu on the selected day
    date = forms.DateField( validators=[current_date],widget=DateInput)
    class Meta:
        model = Menu
        fields = ["date"]
       

class MenuFormset(BaseInlineFormSet):
    """
    The base formset for editing Meals belonging to a Menu
    """
    def add_fields(self, form, index):
        super().add_fields(form, index)

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(''))

    def save(self, commit=True):
       
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        
        if not hasattr(form, 'nested'):
            return False

        if is_form_persisted(form):
            return False

        if not is_empty_form(form):
            return False

        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


#This is the formset for the Meals belonging to a Menu 
MenuMealFormset = inlineformset_factory(
                                Menu,
                                Meal,
                                fields=('content',),
                                extra=1,
                            )
                            
