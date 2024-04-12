from django import forms
from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    """
    Field used to set the last updated time automatically
    """

    def pre_save(self, model_instance, add):
        return timezone.now()


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        frmt = format or "%Y-%m-%d"
        super().__init__(attrs=attrs, format=frmt)


class DateField(forms.DateField):
    """
    DateField that enforces a widget which renders a <input type="date"> element
    """
    widget = DateInput