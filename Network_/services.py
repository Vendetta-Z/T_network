from itertools import chain
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth import login

from .models import User, Posts, UserFollowing, Saved_post
from Like.models import Like
from comments.models import Comments
from videosPost.views import VideoPostView
from comments.serializers import CommentsSchema


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
        postWithVideo = VideoPostView.getAllVideoByAuthor(self, self.user.id)
        postWithoutVideo = Posts.objects.filter(author=self.user)
        AllPostedPublication = list(chain(postWithoutVideo, postWithVideo))
        
        return {
            'user': self.user,
            'subscribes': len(user_subscribes),
            'subscribers': len(user_subscribers),
            'posts': AllPostedPublication

        }


    def change_user_data(self):
        new_data_for_user = self.POST
        user = User.objects.get(id=self.user.id)
        for data in new_data_for_user:
            if new_data_for_user[data] == 'csrfmiddlewaretoken' or new_data_for_user[data] == 'avatar':
                print(self.POST)

                continue
            user.__dict__[data] = new_data_for_user[data]
        print(self.FILES)
        if self.FILES['avatar']:
            user.__dict__['avatar'] = self.FILES['avatar']
        user.save()

        return redirect('/edit_profile')


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
            'author': serializers.serialize('json', [post.author]),
            'Likes':post_likes_len,
            'like_icon': like_icon,
            'comments': json_post_comments,
            'self_user_follow_author': self_user_follow_author
        }


    def get_user_subscribes_data(self):
        UserFollowing.objects.filter(user_id=self.user)


    def save_post_to_favorite(self, post_id):
        post = Posts.objects.get(id=post_id)

        if Saved_post.objects.filter(save_post = post).exists():
            Saved_post.objects.get(user_saved_post = self.user, save_post = post).delete()
            return JsonResponse({'post_status': 'removed'}, safe=False)
        else:
            Save_post = Saved_post(
                user_saved_post = self.user,
                save_post = post
                )
            Save_post.save()
            return JsonResponse({'post_status': 'saved'}, safe=False)



    def get_user_saved_posts(self):
        
        return Saved_post.objects.filter(user_saved_post=self.user)


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


    def change_post_data(Request_POST, request_FILES):
        post_by_id = Posts.objects.get(id=Request_POST['id'])
        post_by_id.__dict__['image'] = request_FILES
        
        for data in Request_POST:
            post_by_id.__dict__[data] = Request_POST[data]
    
        post_by_id.save()
        return JsonResponse('200' , safe=False)


    def delete_post(self, post_id):
        Posts.objects.filter(author=self.user, id=post_id).delete()