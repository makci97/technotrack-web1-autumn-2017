# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default="avatars/user_unknown.png")

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
