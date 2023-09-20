from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import redirect

from .models import User, Posts, UserFollowing

from comments.serializers import CommentsSchema
from comments.models import Comments

from Like.models import Like
from django.contrib.auth import login

class T_network_services:

    def Check_user_exist_and_login(self, username, password):

        user = User.objects.get(username=username, password=password)
        if user:
            login(self, user)
            return redirect('/profile')
        else:
            return JsonResponse({'response': 404, 'message': 'Такой пользователь не найден'})

    def get_user_profile_data(self):
        user_subscribers = UserFollowing.objects.filter(following_user=self.user)
        user_subscribes = UserFollowing.objects.filter(user_id=self.user)
        
        return {
            'user': self.user,
            'subscribes': len(user_subscribes),
            'subscribers': len(user_subscribers),
            'posts': Posts.objects.filter(author=self.user).order_by('-created')

        }

    def get_another_user_profile(self, user):
        user_subscribers = UserFollowing.objects.filter(following_user=user)
        user_subscribes = UserFollowing.objects.filter(user_id=user.id)

        return {
            'user': user,
            'subscribes': len(user_subscribes),
            'subscribers': len(user_subscribers),
            'posts': Posts.objects.filter(author=user).order_by('-created')
        }

    def get_post_data(self, post_id):
        post = Posts.objects.get(id=post_id)
        post_likes_len = len(Like.objects.filter(product=post))

        like_icon = "/static/image/likeHearthicon.png"
        if Like.check_user_liked(self, user=self.user, post=post):
            like_icon = "/static/image/likeHearthicon_after.png"

        post_comments = Comments.objects.filter(post=post).order_by('-created')
        schema = CommentsSchema(many=True)
        json_post_comments = schema.dump(post_comments)


        self_user_follow_author = 0
        follow = UserFollowing.objects.filter(user_id=self.user, following_user=post.author.id)
        if len(follow) > 0:
            self_user_follow_author = 1

        return {
            'post': serializers.serialize('json', [post]),
            # 'author': serializers.serialize('json', [post.author]), возможно понадобиться!!!
            'author': post.author.first_name,
            'Likes':post_likes_len,
            'like_icon': like_icon,
            'comments': json_post_comments,
            'self_user_follow_author': self_user_follow_author
        }


    def get_user_subscribes_data(self):
        UserFollowing.objects.filter(user_id=self.user)


    def subscribe_user(self, user_id):
        subscribed_to_user = User.objects.get(id=user_id)
        if UserFollowing.objects.filter(user_id=self.user, following_user=subscribed_to_user):
            return JsonResponse('вы уже подписались на этого пользователя!', safe=False)
        else:
            newFollowingUser = UserFollowing(
                user_id=self.user,
                following_user=subscribed_to_user,
            )
            newFollowingUser.save()

    def get_user_posts(self, post_autor):
        post_list = Posts.objects.filter(author= post_autor)
        return serializers.serialize('json', post_list)

    def unsubscribe_user(self, following_user_id):
        UserFollowing.unsubscribe(self, following_user_id)
        return JsonResponse({'status_code':200})

    def create_new_post(self, postImage, postDescription):
        Post = Posts(
            author=self.user,
            image=postImage,
            description=postDescription
            )
        Post.save()

        return serializers.serialize('json', [Post])

    def change_post_data(post_id, post_desc, post_img):
        post_by_id = Posts.objects.get(id=post_id)
        post_by_id.description = post_desc
        post_by_id.image = post_img

        try:
            post_by_id.save()
            return JsonResponse('200' , safe=False)
        except:
            return JsonResponse('500', safe=False)

    def delete_post(self, post_id):
        Posts.objects.filter(author=self.user, id=post_id).delete()