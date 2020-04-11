from django.urls import path
from main.views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('game', GameApiView.as_view(), name='game'),
    path('api_token/', obtain_auth_token, name='api_token_auth')
]
