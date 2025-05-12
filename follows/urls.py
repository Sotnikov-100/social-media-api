from django.urls import path
from follows.views import FollowingListView, FollowersListView, FollowUserView


app_name = "follows"

urlpatterns = [
    path("following/", FollowingListView.as_view(), name="following"),
    path("followers/", FollowersListView.as_view(), name="followers"),
    path("user/<int:pk>/follow/", FollowUserView.as_view(), name="follow-user"),
]
