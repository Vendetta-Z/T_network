from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import T_network_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', T_network_views.profile),
    path('<int:id>', T_network_views.get_user_profile),
    path('logout_user', T_network_views.logout),
    path('publication_feed', T_network_views.publication_feed),
    path('subscribe', T_network_views.subscribe, name='subscibe_to'),
    path('user_subscribes', T_network_views.get_user_subscribes, name='user_subscribes'),
    path('unsubscribe', T_network_views.unsubscribe, name='unsubscribe'),
    path('get_post', T_network_views.get_post, name='get_post'),
    path('Post/save_post', T_network_views.save_post_view, name='save_post'),
    path('Post/show_saved_posts', T_network_views.show_saved_views),
    path('get_user_posts', T_network_views.get_user_posts, name='get_all_user_posts'),
    path('change_post_data', T_network_views.change_post_data, name='change_post_data'),
    path('create_new_post', T_network_views.create_post, name='create_new_post'),
    path('delete_post', T_network_views.delete_post, name='delete post'),
    path('Like/' , include('Like.urls')),
    path('Comments/', include('comments.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
