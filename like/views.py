from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from comments.models import Comment
from like.models import Like


def like_it(request):
    user = request.user
    if request.method == 'POST':
        object_id = int(request.POST['object_id'])
        content_type_name = str(request.POST['content_type'])
        like_obj = None

        likes = Like.objects.filter(object_id=object_id)  # in here we filtered the particular post with its id
        if likes and str(user) in str(likes):
                like_obj = Like.objects.get(user=user, object_id=object_id)

        if content_type_name == 'Comment':
            return like_comment(request, object_id, likes, like_obj, user)

    return render(request, 'like/ajaxlike.html', {'likes_count': likes.filter(liked=True).count(), 'okey': 'false'})


def like_comment(request, object_id, likes, like_obj, user):
    content_type = ContentType.objects.get_for_model(Comment.objects.all().first())
    # content_type = ContentType.objects.get(Comment.objects.all().first())
    if str(user) not in str(likes):
        like_obj = Like.objects.create(user=user, liked=True, content_type=content_type, object_id=object_id)
    elif str(user) in str(likes) and like_obj.liked:
        like_obj.liked = False
    elif str(user) in str(likes) and not like_obj.liked:
        like_obj.liked = True
    like_obj.save()

    comment = Comment.objects.all().filter(pk=object_id).first()
    comment.create_like_fields(user)
    context = {'comment': comment}

    return render(request, 'like/like_comment.html', context)
