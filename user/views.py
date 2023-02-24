# Create your views here.
from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Customer
from .serializers import CustomerSerializer, RegisterSerializer


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and request.resolver_match.kwargs.get(
            'pk') is request.user.id


# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": CustomerSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


# Login API
class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        token = Token.objects.get_or_create(user=user)
        return Response({
            "user": CustomerSerializer(user).data,
            "token": token[0].key
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'User Logged out successfully'})


class CustomerViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_object(self):
        return get_object_or_404(Customer, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        if request.user.id != self.kwargs['pk']:
            Response({"message": "invalid Token"}, status=403)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'password' not in request.data:
            return Response({'message': 'password field is empty'}, status=403)
        if not instance.check_password(request.data['password']):
            return Response({'message': 'password is wrong'}, status=403)
        if 'new_password' in request.data:
            instance.set_password(request.data['new_password'])
            instance.save()
        if 'username' in request.data and Customer.objects.filter(~Q(id=instance.id),
                                                                  Q(username=request.data['username'])).count() != 0:
            return Response({"username": "username already exists"}, status=409)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.check_password(request.data['password']):
            return Response({'message': 'password is wrong'}, status=403)
        instance.delete()
        return Response({'message': 'successfully deleted'}, status=204)

    def retrieve(self, request, *args, **kwargs):
        return super(CustomerViewSet, self).retrieve(request, *args, **kwargs)

    def authenticate(self, request):
        if request.user.id != self.kwargs['pk']:
            return False
        return True
