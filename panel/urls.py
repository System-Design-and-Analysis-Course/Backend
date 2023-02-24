from django.urls import re_path

from panel.views import LibraryViewSet

app_name = 'panel'

urlpatterns = [
    # path('<int:user_id>/library/?<int:pk>/',
    #      LibraryViewSet.as_view({'post': 'create', 'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
    #      name='library'),
    re_path(r'^(?P<user_id>[0-9]+)/library/(?:(?P<pk>[0-9]+)/)?$',
            LibraryViewSet.as_view({'post': 'create', 'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}),
            name='library'),
]
