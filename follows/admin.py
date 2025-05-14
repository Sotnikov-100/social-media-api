from django.contrib import admin
from follows.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "created_at")
    list_filter = ("created_at",)
    search_fields = ("follower__username", "followed__username")
