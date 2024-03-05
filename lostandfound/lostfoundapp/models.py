from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class MissingItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    color = models.CharField(max_length=50)
    date_lost = models.DateField()

    def __str__(self):
        return self.name
