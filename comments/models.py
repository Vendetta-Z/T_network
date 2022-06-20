from django.db import models
from Network_.models import User, Posts

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)