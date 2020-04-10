from django.urls import path
from main.views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('hello', HelloView.as_view(), name='hello'),
    path('api_token/', obtain_auth_token, name='api_token_auth')
]
