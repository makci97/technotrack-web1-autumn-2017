from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    liked = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

    @staticmethod
    def get_liked_by_user_and_obj(user, liked_obj):
        if user.is_anonymous:
            return False
        content_type = ContentType.objects.get_for_model(liked_obj)
        like = Like.objects.all().filter(content_type=content_type, object_id=liked_obj.id, user_id=user.id)
        if like.count() == 0 or not like.first().liked:
            return False
        return True

    @staticmethod
    def get_likes_count_by_obj(liked_obj):
        content_type = ContentType.objects.get_for_model(liked_obj)
        return Like.objects.all().filter(content_type=content_type, object_id=liked_obj.id, liked=True).count()

    class Meta:
        ordering = '-id',
        verbose_name = u'Like'
        verbose_name_plural = u'Likes'
