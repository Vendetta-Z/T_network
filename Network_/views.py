from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse

from .services import T_network_services

from .models import User, Posts


class T_network_views:

    def login(self):

        if self.GET:
            username = self.GET.get('firstName')
            password = self.GET.get('password')
            T_network_services.Check_user_exist_and_login(self, username, password)

        return render(self, 'login.html')

    def profile(self):
        if self.user.is_authenticated is False:
            return redirect('/login')

        user_profile_data = T_network_services.get_user_profile_data(self)
        return render(
            self,
            'profile.html',
            user_profile_data
            )

    def get_user_profile(self, id):
        user_by_id =  User.objects.get(id=id)

        user_profile_data = T_network_services.get_another_user_profile(self, user_by_id)

        return render(self, 'profile.html', user_profile_data)





    def logout(self):
        logout(self)
        return render(self, 'login.html')

    def publication_feed(self):
        #TODO перенести всю бизнес логику ленты публикаций в сервисы
        publication = Posts.objects.all().order_by('-created')
        return render(self, 'publication_feed.html',
            {
                'publication_list': publication,
            }
        )

    def get_post(self):
        post_id = self.GET.get('post_id')
        post_data = T_network_services.get_post_data(self, post_id=post_id)

        return JsonResponse(
            post_data,
            safe=False
        )

    def get_user_subscribes(self):
        subs = T_network_services.get_user_subscribes_data(self)
        return render(self, 'user_subscribes.html', {'subscribes': subs})

    def subscribe(self):
        if self.POST:
            user_id = self.POST.get('user_id')
            T_network_services.subscribe_user(self, user_id=user_id)
            return JsonResponse('successfull subscribed!', safe=False)

    def unsubscribe(self):
        if self.POST:
            subscribe_id = self.POST.get('subscribe_id')
            return T_network_services.unsubscribe_user(self, subscribe_id=subscribe_id)
        return redirect('/publication_feed')


    def create_post(self):
        postImage = self.FILES['postImage']
        postDescription = self.POST.get('postDescription')

        Post = T_network_services.create_new_post(self, postImage, postDescription)
        return JsonResponse(Post, safe=False)

    def change_post_data(self):
        print(self.POST)
        print(self.POST)
        print(self.POST)
        print(self)
        print(self)
        print(self.FILES)

        post_id = self.POST['post_id']
        post_description = self.POST['post_description']
        post_image = self.FILES['post_image']
        return T_network_services.change_post_data(post_id, post_description, post_image)
