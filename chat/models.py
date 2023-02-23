from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    msg_id = models.IntegerField()
    body = models.TextField()
    dt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    deleted = models.BooleanField()
    edited = models.BooleanField()


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     ip = models.GenericIPAddressField()


class Contact(models.Model):
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    body = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)

