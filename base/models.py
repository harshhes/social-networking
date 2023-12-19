from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from .manager import CustomUserManager

from enum import Enum

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Status(Enum):
    pending = 'Pending' 
    accepted = 'Accepted' 
    rejected = 'Rejected'
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[(e.value, e.value) for e in Status],
        default=Status.pending.value
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"from: {self.from_user} to: {self.to_user} -> {self.status}"