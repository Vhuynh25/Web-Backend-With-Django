from django.urls import path

from. import views


urlpatterns = [
    path('create', views.create_poll, name='create poll'),
    path('<int:poll_id>', views.get_poll, name='get poll'),
    path('<str:username>/<int:post_id>/<int:choice>', views.post_vote, name='vote on poll'),
    path('all', views.polls, name='polls'),
    path('health', views.check_health, name='health check'),
]