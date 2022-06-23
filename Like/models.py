from django.db import models

from Network_.models import User, Posts

# Create your models here.
class Like(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.OneToOneField(Posts, unique=True, on_delete=models.CASCADE)
    

    def check_user_liked(self, user, post):
        if Like.objects.filter(author=user, product=post).count() == 0: 
            return False
        else:
            return True        