from celery import shared_task
from posts.models import Post


@shared_task
def publish_scheduled_post(post_id):
    try:
        post = Post.objects.get(id=post_id, is_published=False)
        post.is_published = True
        post.save()
        return f"Post {post_id} published"
    except Post.DoesNotExist:
        return f"Post {post_id} does not exist"
