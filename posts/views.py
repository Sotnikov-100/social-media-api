from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from posts.models import Post, Like, Comment
from posts.tasks import publish_scheduled_post
from posts.serializers import (
    PostSerializer,
    PostCreateSerializer,
    LikeSerializer,
    CommentSerializer,
)
from posts.permissions import IsAuthorOrReadOnly


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="List all published posts",
    description="List all published posts with optional hashtag filtering",
)
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)

        hashtag = self.request.query_params.get("hashtag", None)
        if hashtag:
            queryset = queryset.filter(content__icontains=f"#{hashtag}")

        return queryset


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get feed",
    description="Get feed",
)
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        following_users = self.request.user.following.values_list("followed", flat=True)

        return Post.objects.filter(
            Q(author__in=following_users) | Q(author=self.request.user),
            is_published=True,
        )


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get my posts",
    description="Get my posts",
)
class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


@extend_schema(
    tags=["Posts"],
    request=PostCreateSerializer,
    responses={201: PostSerializer},
    summary="Create a new post",
    description="Create a new post",
)
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        if (
            "scheduled_date" in serializer.validated_data
            and serializer.validated_data["scheduled_date"]
        ):
            publish_scheduled_post.apply_async(
                args=[serializer.instance.id],
                eta=serializer.validated_data["scheduled_date"],
            )


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get post details",
    description="Get post details",
)
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Like a post",
    description="Like a post",
)
class LikePostView(APIView):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "You have already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LikeSerializer(like, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(
                {"detail": "You have successfully unliked the post"},
                status=status.HTTP_200_OK,
            )
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get liked posts",
    description="Get liked posts",
)
class LikedPostsView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        liked_posts_ids = self.request.user.likes.values_list("post", flat=True)
        return Post.objects.filter(id__in=liked_posts_ids, is_published=True)


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get comments",
    description="Get comments",
)
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(user=self.request.user, post=post)


@extend_schema(
    tags=["Posts"],
    responses={200: PostSerializer},
    summary="Get comment details",
    description="Get comment details",
)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
