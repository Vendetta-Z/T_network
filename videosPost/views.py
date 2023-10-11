from django.shortcuts import render
from .models import Video_post


class VideoPostView():

    def getAllVideoByAuthor(self, author):
        return Video_post.objects.filter(author=author)
    
    def getVideoByID(self, author, videoID):
        return Video_post.objects.filter(author=author, id=videoID)
        