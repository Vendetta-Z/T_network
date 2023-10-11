from django.contrib import admin
from .models import User
from .models import Posts
from videosPost.models import Video_post

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Video_post)