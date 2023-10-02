from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django import forms

from Newtwork.settings import SECRET_KEY
from .services import T_network_services
from .models import User, Posts


class T_network_views:

    def profile(self):
        if self.user.is_authenticated is False:
            return render(self, 'login.html')
        
        user_profile_data = T_network_services.get_user_profile_data(self)
        print(SECRET_KEY)

        return render(
            self,
                'profile_copy.html',
                user_profile_data
            )


    def get_user_profile(self, id):
        user_by_id =  User.objects.get(id=id)
        user_profile_data = T_network_services.get_another_user_profile(self, user_by_id)

        return render(self, 'another_user_profile.html', user_profile_data)


    def edit_profile(self):
        return render(self, 'edit_profile.html')


    def change_user_data(self):
        if self.POST:
            return T_network_services.change_user_data(self)

            
    def save_post_view(self):
        post_id = self.POST.get('saved_post_id')
        return T_network_services.save_post_to_favorite(self, post_id)


    def show_saved_views(self):
        saved_posts = T_network_services.get_user_saved_posts(self)
        return render(self, 'favorite_saved_post.html', { 'saved_posts': saved_posts})


    def get_user_posts(self):
        author_id = self.GET.get('post_author')
        posts = T_network_services.get_user_posts(self, author_id)
        return JsonResponse(posts, safe=False)


    def logout(self):
        logout(self)
        return render(self, 'login.html')


    def publication_feed(self):
        #TODO перенести всю бизнес логику ленты публикаций в сервисы
        publication = Posts.objects.all().order_by('-created')

        return render(self, 'publication_feed.html', { 'publication_list' : publication } )


    def get_post(self):
        post_id = self.GET.get('post_id')
        post_data = T_network_services.get_post_data(self, post_id=post_id)

        return JsonResponse(
            post_data,
            safe=False
        )


    def get_user_subscribes(self):
        subscribers = T_network_services.get_user_subscribes_data(self)
        return render(self, 'user_subscribes.html', {'subscribes': subscribers})


    def subscribe(self):
        if self.POST:
            user_id = self.POST.get('user_id')
            T_network_services.subscribe_user(self, user_id=user_id)
            return JsonResponse('successfull subscribed!', safe=False)


    def unsubscribe(self):
        if self.POST:
            following_user_id = self.POST.get('following_user_id')
            return T_network_services.unsubscribe_user(self, following_user_id)
        return redirect('/publication_feed')


    def create_post(self):
        postImage = self.FILES['postImage']
        postDescription = self.POST.get('postDescription')

        Post = T_network_services.create_new_post(self, postImage, postDescription)
        return JsonResponse(Post, safe=False)


    def change_post_data(self):
        request_POST = self.POST
        request_FILES = self.FILES['post_image']
        return T_network_services.change_post_data(request_POST, request_FILES)


    def delete_post(self):
        post_id = self.POST['post_id']
        T_network_services.delete_post(self, post_id)
        return JsonResponse('post succesfull deleted!', safe=False)