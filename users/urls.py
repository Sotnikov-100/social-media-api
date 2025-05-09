from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import RegisterView, UserProfileView, UserSearchView, UserDetailView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("search/", UserSearchView.as_view(), name="search"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
