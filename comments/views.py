from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Comments

from Network_.models import Posts


class CommentsViews:

    def new_comment(self):
        post = Posts.objects.get(id=self.POST.get('post_id'))
        comm_msg = self.POST.get('comm_text')
        comm = Comments( author=self.user, post=post, text=comm_msg)
        comm.save()
        return JsonResponse({
            'status_code': 200,
            'author': comm.author.first_name,
            'text': comm.text,
            'created': comm.created
        })
