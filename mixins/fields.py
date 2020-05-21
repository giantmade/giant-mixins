from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    """
    Field used to set the last updated time automatically
    """

    def pre_save(self, model_instance, add):
        return timezone.now()
