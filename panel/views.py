from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from panel.models import Library
from panel.serializers import LibrarySerializer


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and \
               int(request.resolver_match.kwargs.get('user_id')) is int(request.user.id)


class LibraryViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return get_object_or_404(Library, pk=self.kwargs['pk'])

    def get_queryset(self):
        return Library.objects.filter(user__id=self.kwargs['user_id'])

    def retrieve(self, request, *args, **kwargs):
        if 'pk' not in self.kwargs:
            return super(LibraryViewSet, self).list(request, *args, **kwargs)
        return super(LibraryViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        library = self.get_object()
        if 'content_type' in request.data and library.file_set.count() != 0:
            return Response({'message': 'can\'t update content type of an existing library'}, status=403)
        if 'date_info' in request.data:
            return Response({'message': 'can\'t update date_info of an existing library'}, status=403)
        return super(LibraryViewSet, self).update(request, *args, **kwargs)
