from django.db import models
from django.contrib.auth.models import User


class HydroponicSystem(models.Model):
    id = models.AutoField(primary_key=True)
    system_name = models.CharField()
    description = models.CharField(default=None, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
