from django.urls import path
from .views import CommentsViews


urlpatterns = [
    path('new_comment', CommentsViews.new_comment, name='new comment')
]