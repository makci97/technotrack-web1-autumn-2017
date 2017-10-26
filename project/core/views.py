from django.shortcuts import render

from blog.models import Blog
from comments.models import Comment
from post.models import Post


def index(request):
    context = {
        'Blog_count': Blog.objects.all().count(),
        'Post_count': Post.objects.all().count(),
        'Comment_count': Comment.objects.all().count()
    }
    return render(request, 'core/index.html', context)
