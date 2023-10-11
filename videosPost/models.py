from django.db import models
from django.core.validators import FileExtensionValidator
from Network_.models import User

# Create your models here.
class Video_post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=128, null=False)   потом добавить в постах 
    video = models.FileField( upload_to='videoposts/' ,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    description= models.CharField(max_length=528, null=False)
    created= models.DateTimeField(auto_now=True)
    views = 'a'#Тут будут посмотры

    def __str__(self):
        return self.name