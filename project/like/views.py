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
        if likes:  # if the particular post is there
            if str(user) in str(likes):  # then we check the user which is us, in there
                like_obj = Like.objects.get(user=user,
                                            object_id=object_id)
                # if we there and we returned this data, this part for saving data,
                # I mean if this data is already created than we dont have to delete and create again,
                # we just change Like.liked true or false state, so that if you create like and it will never delete,
                # it just change liked or like state
            else:
                pass

        if content_type_name == 'Comment':
            # comment_content_type_name_by = Comment.objects.all().first()
            # print(comment_content_type_name_by.get_content_type_name())
            content_type = ContentType.objects.get(app_label="comments", model="Comment")
            print(content_type)

            if str(user) not in str(likes):
                like = Like.objects.create(user=user, liked=True, content_type=content_type, object_id=object_id)
                like.save()  # if data is created then we say 'new'
                okey = 'new'

            elif str(user) in str(likes) and like_obj.liked:
                like_obj.liked = False
                like_obj.save()  # if data is already there, then we save it False
                okey = 'false'

            elif str(user) in str(likes) and like_obj.liked == False:
                like_obj.liked = True
                like_obj.save()  # if data is already changed to False and we save again to True
                okey = 'true'

    return render(request, 'like/ajaxlike.html', {'likes_count': likes.count(), 'okey': okey})
