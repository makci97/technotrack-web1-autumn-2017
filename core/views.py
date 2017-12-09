from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView, CreateView

from blog.forms import BlogsListForm
from blog.models import Blog
from comments.models import Comment
from core.forms import UserEditForm
from core.models import Category
from post.forms import PostsListForm
from post.models import Post


def index(request):
    context = {
        'Blog_count': Blog.objects.all().count(),
        'Post_count': Post.objects.all().count(),
        'Comment_count': Comment.objects.all().count(),
    }
    return render(request, 'core/index.html', context)


def about(request):
    context = {}
    return render(request, 'core/about.html', context)


def contacts(request):
    context = {}
    return render(request, 'core/contacts.html', context)


class UserPostsList(ListView):
    model = Post
    template_name = "user/user_page_posts_list.html"
    context_object_name = 'posts'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(get_user_model().objects.all(), id=kwargs.get('pk'))
        return super(UserPostsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(UserPostsList, self).get_queryset()
        self.form = PostsListForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['order_by']:
                queryset = queryset.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                queryset = queryset.filter(title__contains=self.form.cleaned_data['search'])
        return queryset.filter(author_id=self.author.id)

    def get_context_data(self, **kwargs):
        context = super(UserPostsList, self).get_context_data(**kwargs)
        context['author'] = self.author
        context['form'] = self.form
        context['blogs_count'] = Blog.objects.all().filter(author_id=self.author.id).count()
        context['posts_count'] = Post.objects.all().filter(author_id=self.author.id).count()
        context['can_edit'] = (
            self.request.user.id == self.author.id
        )
        return context


class UserBlogsList(ListView):
    model = Blog
    template_name = "user/user_page_blogs_list.html"
    context_object_name = 'blogs'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(get_user_model().objects.all(), id=kwargs.get('pk'))
        return super(UserBlogsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(UserBlogsList, self).get_queryset()
        self.form = BlogsListForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['order_by']:
                queryset = queryset.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                queryset = queryset.filter(title__contains=self.form.cleaned_data['search'])
        return queryset.filter(author_id=self.author.id)

    def get_context_data(self, **kwargs):
        context = super(UserBlogsList, self).get_context_data(**kwargs)
        context['author'] = self.author
        context['form'] = self.form
        context['blogs_count'] = Blog.objects.all().filter(author_id=self.author.id).count()
        context['posts_count'] = Post.objects.all().filter(author_id=self.author.id).count()
        context['can_edit'] = (
            self.request.user.id == self.author.id
        )
        return context


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class UserEdit(UpdateView):
    template_name = 'user/edit_user.html'
    model = get_user_model()
    form_class = UserEditForm

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(UserEdit, self).dispatch(request, *args, **kwargs)
        except PermissionDenied:
            return HttpResponseForbidden()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.id != obj.id:
            raise PermissionDenied()
        return obj

    # def get_context_data(self, **kwargs):
    #     context = super(UserEdit, self).get_context_data(**kwargs)
    #     context['blog_id'] = self.object.blog.id
    #     return context

    def get_success_url(self):
        return reverse('core:user_blogs_list', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class NewCategory(CreateView):
    template_name = 'category/new_category.html'
    model = Category
    fields = ('title', )

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        print(next_url)
        if next_url:
            return next_url
        else:
            return reverse('core:index')
