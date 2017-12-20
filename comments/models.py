# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from like.models import Like
from post.models import Post


class Comment(models.Model):
    #а вот собственно привязка коммента к посту
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    likes = GenericRelation(Like, related_query_name='likes')
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return u'{}\n{}: {}'.format(self.created_at, self.author, self.text)

    def create_like_fields(self, user):
        self.likes_count = Like.get_likes_count_by_obj(self)
        self.is_liked = Like.get_liked_by_user_and_obj(user, self)

    def like_add(self):
        self.likes_count += 1

    def like_del(self):
        self.likes_count -= 1

    class Meta:
        ordering = '-id',
        verbose_name = u'Comment'
        verbose_name_plural = u'Comments'