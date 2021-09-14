from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from PIL import Image
from notification.models import Notification

from Admin_app.utils import auto_save_current_user
# Create your models here.

User = settings.AUTH_USER_MODEL 

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null = True, blank=True)
    phone = models.CharField(max_length=50)

    @property
    def follower_count(self):
        count = self.follow_followed.count()
        return count

    @property
    def following_count(self):
        count = self.follow_follower.count()
        return count
    
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE,  related_name="student")
    student_id = models.CharField(max_length=50)
    level_term = models.ForeignKey('Level_Term', on_delete=models.CASCADE, null = True, blank=True)
    
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name="teacher")  
    teacher_id = models.CharField(max_length=50)
    designation = models.ForeignKey('Designation', on_delete=models.CASCADE, null = True, blank=True)
    def __str__(self):
        return self.user.username

class Department(models.Model):
    department_name = models.CharField(max_length=50)
    def __str__(self):
        return self.department_name

class Level_Term(models.Model):
    level_term_name = models.CharField(max_length=20)
    def __str__(self):
        return self.level_term_name


class Designation(models.Model):
    designation_name = models.CharField(max_length=20)
    def __str__(self):
        return self.designation_name

# Followers Model
class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(User, related_name='follow_followed', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user} --> {self.followed}"

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Follow, self).save(*args, **kwargs)
    
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.user
        followed = follow.followed
        notify = Notification(sender=sender, user=followed, notification_type=2)
        notify.save()
        
    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.user
        followed = follow.followed

        notify = Notification.objects.filter(sender=sender, user=followed, notification_type=2)
        notify.delete()



	



#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)