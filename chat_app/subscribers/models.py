from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SubscribeModel(models.Model):
    self_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers_self_user')
    other_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='subscribers_other_user')