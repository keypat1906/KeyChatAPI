from django.urls import path
from . import views


urlpatterns = [
    path('api/messages/<int:receiver>/<int:sender>', views.message_list, name='message-detail'),
    path('api/recent-messages', views.message_all, name='message-all'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
]
