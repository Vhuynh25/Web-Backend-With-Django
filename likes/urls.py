from django.urls import path

from. import views


urlpatterns = [
    path('<str:liker_username>/<str:username>/<int:post_id>', views.like, name='like post'),
    path('<str:username>/<int:post_id>', views.like_counts, name='user likes posts'),
    path('<str:user>', views.user_liked, name='user likes count'),
    path('popular', views.popular_post, name='popular posts'),
    path('health', views.check_health, name='health check'),
]