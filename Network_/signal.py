from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount# step 3 made this possible
from .models import User


@receiver(post_save, sender = SocialAccount)
def create_user_if_google_login(sender, instance, created, **kwargs):
    if created:
        user = User(
            first_name = instance.user.first_name,
            last_name = instance.user.last_name ,
            avatar = instance.extra_data['picture']
        )
        user.save()
  