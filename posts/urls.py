from django.urls import path
from posts.views import (
    PostListView,
    PostCreateView,
    FeedView,
    MyPostsView,
    LikedPostsView,
    PostDetailView,
    LikePostView,
    CommentListView,
    CommentDetailView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("my/", MyPostsView.as_view(), name="my-posts"),
    path("liked/", LikedPostsView.as_view(), name="liked-posts"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("<int:pk>/comments/", CommentListView.as_view(), name="post-comments"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
