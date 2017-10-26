from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from core.forms import SignUpForm
from blog.models import Blog
from comments.models import Comment
from post.models import Post


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:index')
    else:
        form = SignUpForm()
    return render(request, 'core/sign_up.html', {'form': form})


def index(request):
    context = {
        'Blog_count': Blog.objects.all().count(),
        'Post_count': Post.objects.all().count(),
        'Comment_count': Comment.objects.all().count()
    }
    return render(request, 'core/index.html', context)
