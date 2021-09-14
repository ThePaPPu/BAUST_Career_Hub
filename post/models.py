from django.conf import settings
from django.db import models
from django.urls import reverse
from notification.models import Notification
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) 
    descriptions = models.TextField(max_length=1000)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.descriptions
    
    # def comment_count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'
    
    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.content[:90]
        sender = comment.user
        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=1)
        notify.save()

post_save.connect(Comment.user_comment_post, sender=Comment)