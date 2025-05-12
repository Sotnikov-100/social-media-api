from rest_framework import serializers
from posts.models import Post, Like, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content", "created_at", "updated_at")
        read_only_fields = ("post",)


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post", "created_at")
        read_only_fields = ("post",)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "image",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "is_liked",
            "scheduled_date",
        )
        read_only_fields = ("author",)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    scheduled_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Post
        fields = ("content", "image", "scheduled_date")

    def create(self, validated_data):
        if "scheduled_date" in validated_data and validated_data["scheduled_date"]:
            validated_data["is_published"] = False

        return super().create(validated_data)
