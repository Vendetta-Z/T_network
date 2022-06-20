from django.urls import path
from .views import LikeViews

urlpatterns = [
    path('add_like', LikeViews.add_like, name='Add_like')
]