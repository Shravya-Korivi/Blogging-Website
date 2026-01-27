from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, BlogPost, Comment, Notification, Follow

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.followed,
            sender=instance.follower,
            notification_type='follow'
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # If it's a reply to another comment
        if instance.parent:
            # Notify the parent comment author
            if instance.parent.author != instance.author:
                Notification.objects.create(
                    recipient=instance.parent.author,
                    sender=instance.author,
                    notification_type='reply',
                    post=instance.post,
                    comment=instance
                )
        # If it's a direct comment on a post
        else:
            # Notify the post author
            if instance.post.author != instance.author:
                Notification.objects.create(
                    recipient=instance.post.author,
                    sender=instance.author,
                    notification_type='comment',
                    post=instance.post,
                    comment=instance
                )

@receiver(m2m_changed, sender=BlogPost.likes.through)
def create_post_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            user = User.objects.get(pk=pk)
            if user != instance.author:
                Notification.objects.create(
                    recipient=instance.author,
                    sender=user,
                    notification_type='like_post',
                    post=instance
                ) 