# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from like.models import Like
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
        return u'{}\n{}: {}'.format(self.created_at, self.author, self.text)

    def get_liked_by_user(self, user):
        if user.is_anonymous:
            return False
        content_type = ContentType.objects.get(app_label="comments", model="Comment")
        like = Like.objects.all().filter(content_type=content_type, object_id=self.id)
        if like.count() == 0 or not like.first().liked:
            return False
        return True

    def get_likes_count(self):
        content_type = ContentType.objects.get(app_label="comments", model="Comment")
        return Like.objects.all().filter(content_type=content_type, object_id=self.id).count()

    class Meta:
        ordering = '-id',
        verbose_name = u'Comment'
        verbose_name_plural = u'Comments'