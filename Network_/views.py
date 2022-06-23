from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.core import serializers
from Like.models import Like
from comments.models import Comments

from comments.serializers import CommentsSchema

from .models import User, UserFollowing, Posts


class T_network_views:

    def login(self):

        if self.GET:
            username = self.GET.get('firstName')
            password = self.GET.get('password')
            user = User.objects.get(first_name=username, password=password)
            if user:
                login(self, user)
                return redirect('/profile')
            else:
                return JsonResponse({'response': 404, 'message': 404})

        return render(self, 'login.html')

    def profile(self):
        if self.user.is_authenticated is False:
            return redirect('/login')

        user_subscribers = UserFollowing.objects.filter(following_user=self.user)
        user_subscribes = UserFollowing.objects.filter(user_id=self.user)
        return render(self, 'profile.html', {
            'user': self.user,
            'subscribes': len(user_subscribes),
            'subscribers': len(user_subscribers),
            'posts': Posts.objects.filter(avtor=self.user).order_by('-created')

        })

    def logout(self):
        logout(self)
        return render(self, 'login.html')

    def publication_feed(self):
        users = User.objects.all() 

        return render(self, 'publication_feed.html', {'users': users})

    def get_post(self):
        post = Posts.objects.get(id=self.GET.get('post_id'))
        post_likes_len = len(Like.objects.filter(product=post))
        
        like_icon = "/static/image/likeHearthicon.png"
        if Like.check_user_liked(self, user=self.user, post=post):
            like_icon = "/static/image/likeHearthicon_after.png"
        
        post_comments =  Comments.objects.filter(post=post)
        # Конвертация объектов класса Comments в json при помощи marshmallow
        schema = CommentsSchema(many=True)
        json_post_comments = schema.dump(post_comments)
        
        return JsonResponse({
                'post': serializers.serialize('json', [post]),
                'Likes':post_likes_len,
                'like_icon': like_icon,
                'comments': json_post_comments
            },
            safe=False
        )

    def get_user_subscribes(self):
        subs = UserFollowing.objects.filter(user_id=self.user)

        return render(self, 'user_subscribes.html', {'subscribes': subs})

    def subscribe(self):
        if self.POST:
            user_id = self.POST.get('user_id')
            subscribed_to_user = User.objects.get(id=user_id)
            if UserFollowing.objects.filter(user_id=self.user, following_user=subscribed_to_user):
                return JsonResponse('вы уже подписались на этого пользователя!', safe=False)
            else:
                UserFollowing.objects.create(
                    user_id=self.user,
                    following_user=subscribed_to_user,
                )
            return JsonResponse('successfull subscribed!', safe=False)

    def unsubscribe(self):
        if self.POST:
            subscribe_id = self.POST.get('subscribe_id')
            UserFollowing.unsubscribe(self, subscribe_id)
            return JsonResponse({'status_code':200})
        return redirect('/publication_feed')


    def create_post(self):
        postImage = self.FILES['postImage']
        postDescription = self.POST.get('postDescription')
        

        Post = Posts(
            avtor=self.user,
            image=postImage,
            description=postDescription
            )
        Post.save()
        # Post.avtor = self.user
        # Post.image = postImage
        # Post.description = postDescription 
        # Post.save()
        lastAddedPost = Post
        return JsonResponse(serializers.serialize('json', [Post]), safe=False)