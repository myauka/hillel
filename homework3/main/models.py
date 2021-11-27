from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User


class UrlFromUser(models.Model):
    short_url = models.CharField(max_length=256)
    link = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             blank=True, null=True)
    redirect_count = models.IntegerField(default=0)

# Create your models here.
