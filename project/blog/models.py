# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from core.models import Category


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, verbose_name=u'Blog theme')
    categories = models.ManyToManyField(Category, related_name='blogs')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = '-id',
        verbose_name = u'Blog'
        verbose_name_plural = u'Blogs'
