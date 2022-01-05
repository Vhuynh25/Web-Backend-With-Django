from django.urls import path


from. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/post', views.create_post, name='create post'),
    path('<str:user>/<int:post_id>', views.get_post, name='user post'),
    path('<str:user>', views.timeline, name='user posts'),
    path('public', views.public, name='public'),
    path('health', views.check_health, name='health check'),
]
