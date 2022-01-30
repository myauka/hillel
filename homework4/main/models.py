from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
# from django.conf import settings
from django.contrib.auth.models import User


# class UrlFromUser(models.Model):
#     short_url = models.CharField(max_length=256)
#     link = models.URLField()
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#                              blank=True, null=True)
#     redirect_count = models.IntegerField(default=0)
# title (заголовок)
# text (тело поста)
# slug
# created_by (ссылка на автора)
# created_at (дата/время создания)


class UserPost(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('user_post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
# Create your models here.
