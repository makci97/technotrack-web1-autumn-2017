# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from post.models import Post


class Comment(models.Model):
    #а вот собственно привязка камента к посту
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return u'{} ({})'.format(self.author, self.text)

    class Meta:
        ordering = '-id',
        verbose_name = u'Comment'
        verbose_name_plural = u'Comments'