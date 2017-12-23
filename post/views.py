from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, ListView
from django.db import models

from blog.models import Blog
from comments.models import Comment
from post.forms import PostsListForm
from post.models import Post


def post_detail(request, pk):
    # post = get_object_or_404(Post.objects.all(), id=pk)
    post = Post.objects.filter(id=pk).select_related('blog__author', 'author').first()
    if post is None:
        return Http404('No post matches the given query.')
    context = {'post': post}
    context['post_id'] = post.id
    context['can_edit'] = (
        request.user.id == post.blog.author.id
    )
    context['comments'] = Comment.objects.all().filter(
            models.Q(post_id=post.id) & (models.Q(is_deleted=False) | models.Q(post__author_id=request.user.id))
        ).annotate(
        # likes_count=models.Sum(
        #     models.Case(
        #         models.When(likes__liked=True, then=1),
        #         default=0, output_field=models.IntegerField()
        #     )
        # ),
        is_liked=models.Sum(
            models.Case(
                models.When(likes__liked=True, likes__user_id=request.user.id, then=1),
                default=0, output_field=models.IntegerField()
            ), output_field=models.BooleanField()
        ),
        is_invisible=models.Case(
            models.When(models.Q(is_deleted=True) & models.Q(post__author_id=request.user.id), then=True),
            default=False, output_field=models.BooleanField()
        )
    )
    context['author'] = post.author
    # context['comments'] = Comment.objects.all().filter(post_id=post.id)
    # for comment in context['comments']:
    #     comment.create_like_fields(request.user)
    return render(request, 'post/post_page.html', context)


class NewPost(CreateView):
    template_name = 'post/new_post.html'
    model = Post
    fields = 'title', 'text', 'categories'

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), id=blog_id)
        can_create = self.request.user.id == self.blog.author.id
        if not can_create:
            return HttpResponseForbidden()
        return super(NewPost, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewPost, self).get_context_data(**kwargs)
        context['blog_id'] = self.blog.id
        return context

    # def get_success_url(self):
    #     return reverse('post:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.blog
        return super(NewPost, self).form_valid(form)


class EditPost(UpdateView):
    template_name = 'post/edit_post.html'
    model = Post
    fields = 'title', 'text', 'categories'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(EditPost, self).dispatch(request, *args, **kwargs)
        except PermissionDenied:
            return HttpResponseForbidden()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.id != obj.blog.author.id:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['blog_id'] = self.object.blog.id
        return context

    # def get_success_url(self):
    #  return reverse('post:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.object.blog
        return super(EditPost, self).form_valid(form)


class PostList(ListView):
    model = Post
    template_name = "post/posts_list.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        self.form = PostsListForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['order_by']:
                queryset = queryset.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                queryset = queryset.filter(title__contains=self.form.cleaned_data['search'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['posts_count'] = context['posts'].count()
        # context['posts_count'] = Post.objects.all().count()
        context['form'] = self.form
        return context

