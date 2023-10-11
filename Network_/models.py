from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    status = models.CharField(max_length=120, default='Hi i\'m use a TarVin', null=False)
    avatar = models.ImageField(default='image/default_avatar.png', upload_to='Network_/static/avatar')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Saved_post(models.Model):
    user_saved_post = models.ForeignKey(User, on_delete=models.CASCADE)
    save_post = models.OneToOneField(Posts, unique=True,on_delete=models.CASCADE)
    saved_time = models.DateTimeField(auto_now=True)


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

