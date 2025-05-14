from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from follows.models import Follow
from follows.serializers import FollowSerializer, FollowCreateSerializer
from users.serializers import UserSerializer


@extend_schema(
    request=FollowCreateSerializer,
    responses=FollowSerializer,
    tags=["follows"],
    summary="Follow a user",
    description="Follow a user",
)
class FollowUserView(APIView):

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user, followed=user_to_follow
        )

        if not created:
            return Response(
                {"detail": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user_to_unfollow = get_object_or_404(User, pk=pk)

        try:
            follow = Follow.objects.get(
                follower=request.user, followed=user_to_unfollow
            )
            follow.delete()
            serializer = FollowSerializer(follow)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response(
                {"detail": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    responses=UserSerializer,
    tags=["follows"],
    summary="Get following users",
    description="Get following users",
)
class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(followers__follower=self.request.user)


@extend_schema(
    responses=UserSerializer,
    tags=["follows"],
    summary="Get followers users",
    description="Get followers users",
)
class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(following__followed=self.request.user)
