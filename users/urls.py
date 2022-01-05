from django.urls import path

from. import views

urlpatterns = [
    path('<int:user_id>/<str:password>', views.get_password, name='get password'),
    path('<str:user>/followers', views.get_follows, name='user follows'),
    path('<str:username>', views.user_request, name='user requests'),
    path('', views.get_users, name='all users'),
    path('health', views.check_health, name='health check'),
]
