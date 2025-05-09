from django.contrib import admin
from posts.models import Post, Like, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "content_short",
        "created_at",
        "is_published",
        "scheduled_date",
    )
    list_filter = ("is_published", "created_at", "author")
    search_fields = ("content", "author__username")
    date_hierarchy = "created_at"

    def content_short(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_short.short_description = "Content"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post_short", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__content")

    def post_short(self, obj):
        return (
            obj.post.content[:50] + "..."
            if len(obj.post.content) > 50
            else obj.post.content
        )

    post_short.short_description = "Post"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post_short", "content_short", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__content", "content")

    def post_short(self, obj):
        return (
            obj.post.content[:50] + "..."
            if len(obj.post.content) > 50
            else obj.post.content
        )

    post_short.short_description = "Post"

    def content_short(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_short.short_description = "Content"
