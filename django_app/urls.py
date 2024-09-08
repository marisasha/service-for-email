from django.urls import path
from django_app import views , views_a


urlpatterns = [
    path('',views.login_user,name = 'login'),
    path('register',views.register,name = 'register'),
    path('logout',views.logout_user,name = 'logout'),


    path('home',views.home,name = 'home'),
    path('message',views.message,name = 'message'),
]

websocket_urlpatterns = [
    path("ws/messages", views_a.EmailConsumer.as_asgi())
    ]