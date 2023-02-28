from dataclasses import fields
from pydoc import describe
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.CharField(max_length=120, default='fuck it\'s T_network', null=False)
    avatar = models.ImageField(upload_to='Network_/static/avatar/')



class UserFollowing(models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE, related_name='subscribe_to')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribed')

    def unsubscribe(self, following_user_id):
        user_subscribe = UserFollowing.objects.filter(user_id = self.user ,following_user_id=following_user_id)
        user_subscribe.delete()

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=350)
    image = models.ImageField(upload_to='Network_/static/publication_image')
    created = models.DateTimeField(auto_now=True)