from django.urls import path
from user.views import RegisterAPI, LoginAPI

app_name = 'user'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
]
