from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from panel.models import Library, File, CustomDate, Attachment
from panel.serializers import LibrarySerializer, FileSerializer, AttachmentSerializer
from user.models import Customer


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


class FileViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return get_object_or_404(File, pk=self.kwargs['pk'])

    def get_queryset(self):
        return File.objects.filter(user__id=self.kwargs['user_id'], libraries__id=self.kwargs['library_id'])

    def retrieve(self, request, *args, **kwargs):
        if 'pk' not in self.kwargs:
            return super(FileViewSet, self).list(request, *args, **kwargs)
        return HttpResponse(self.get_object().content)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(Customer, pk=self.kwargs['user_id'])
        library = get_object_or_404(Library, pk=self.kwargs['library_id'])
        date_info = CustomDate(created_at=now(), last_modified_at=now())
        date_info.save()
        file = File(name=request.FILES['content'].name, content_type=library.content_type, user=user,
                    date_info=date_info,
                    content=request.FILES['content'])
        file.save()
        file.libraries.add(library)
        serialized_data = self.get_serializer(file)
        return Response(serialized_data.data, status=200)


class AttachmentViewSet(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return get_object_or_404(Attachment, pk=self.kwargs['pk'])

    def get_queryset(self):
        return Attachment.objects.filter(file__id=self.kwargs['file_id'])

    def retrieve(self, request, *args, **kwargs):
        if 'pk' not in self.kwargs:
            return super(AttachmentViewSet, self).list(request, *args, **kwargs)
        obj = self.get_object()
        if obj.content:
            return HttpResponse(self.get_object().content)
        return Response({'message': 'attachment has no content to download'}, status=404)

    def create(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=self.kwargs['file_id'])
        date_info = CustomDate(created_at=now(), last_modified_at=now())
        date_info.save()
        if 'content' in request.data:
            attachment = Attachment(name=request.data['name'], file=file,
                                    date_info=date_info,
                                    content=request.FILES['content'])
        else:
            attachment = Attachment(name=request.data['name'], file=file,
                                    date_info=date_info,
                                    value=request.data['value'])
        attachment.save()
        serialized_data = self.get_serializer(attachment)
        return Response(serialized_data.data, status=200)
