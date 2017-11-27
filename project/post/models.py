# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from blog.models import Blog
from core.models import Category


class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, default='')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return u'{} ({})'.format(self.id, self.text)

    class Meta:
        ordering = '-id',
        verbose_name = u'Post'
        verbose_name_plural = u'Posts'