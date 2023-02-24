from django.urls import path

from user.views import RegisterAPI, LoginAPI, CustomerViewSet

app_name = 'user'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/<int:pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
         name='profile'),
]
