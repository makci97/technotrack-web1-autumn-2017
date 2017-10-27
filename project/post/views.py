from django.shortcuts import reverse, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from blog.models import Blog
from post.models import Post


class PostDetail(DetailView):
    template_name = 'post/post_page.html'
    context_object_name = 'post'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['can_edit'] = (
            self.request.user.id == self.object.blog.author.id == self.object.author.id
        )
        return context


class NewPost(CreateView, UserPassesTestMixin):
    template_name = 'post/new_post.html'
    model = Post
    fields = 'title', 'text', 'categories'

    def test_func(self):
        return self.can_create

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), id=blog_id)
        self.can_create = (
            self.request.user.id == self.blog.author.id
        )
        return super(NewPost, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewPost, self).get_context_data(**kwargs)
        context['blog_id'] = self.blog.id
        return context

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.blog
        return super(NewPost, self).form_valid(form)


class EditPost(UpdateView, UserPassesTestMixin):
    template_name = 'post/edit_post.html'
    model = Post
    fields = 'title', 'text', 'categories'


    def test_func(self):
        return (
            self.request.user.id == self.blog.author.id == self.object.author.id
        )

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), id=blog_id)
        return super(EditPost, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['blog_id'] = self.blog.id
        return context

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.blog
        return super(EditPost, self).form_valid(form)
