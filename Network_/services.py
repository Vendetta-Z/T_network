from django.http import JsonResponse
from django.core import serializers

from .models import User, Posts, UserFollowing
from .serializers import PostsSchema

from comments.serializers import CommentsSchema
from comments.models import Comments

from Like.models import Like


class T_network_services:

    def Check_user_exist_and_login(self, username, password):

        user = User.objects.get(first_name=username, password=password)
        if user:
            login(self, user)
            return redirect('/profile')
        else:
            return JsonResponse({'response': 404, 'message': 404})

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

        return {
            'post': serializers.serialize('json', [post]),
            # 'author': serializers.serialize('json', [post.author]), возможно понадобиться!!!
            'author': post.author.first_name,
            'Likes':post_likes_len,
            'like_icon': like_icon,
            'comments': json_post_comments
        }

    
    def get_user_subscribes_data(self):
        UserFollowing.objects.filter(user_id=self.user)


    def subscribe_user(self, user_id):
        subscribed_to_user = User.objects.get(id=user_id)
        if UserFollowing.objects.filter(user_id=self.user, following_user=subscribed_to_user):
            return JsonResponse('вы уже подписались на этого пользователя!', safe=False)
        else:
            UserFollowing.objects.create(
                user_id=self.user,
                following_user=subscribed_to_user,
            )

    def unsubscribe_user(self, subscribe_id):
        UserFollowing.unsubscribe(self, subscribe_id)
        return JsonResponse({'status_code':200})

    def create_new_post(self, postImage, postDescription):
        Post = Posts(
            author=self.user,
            image=postImage,
            description=postDescription
            )
        Post.save()

        return serializers.serialize('json', [Post])