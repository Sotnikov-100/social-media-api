from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions
from users.models import UserProfile
from users.serializers import (
    UserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


@extend_schema(request=RegisterSerializer)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


@extend_schema(request=UserProfileUpdateSerializer)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UserProfileUpdateSerializer
        return UserProfileSerializer


@extend_schema(request=UserSerializer)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(request=UserSerializer)
class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["username", "email", "profile__bio"]
    filter_backends = [SearchFilter]
