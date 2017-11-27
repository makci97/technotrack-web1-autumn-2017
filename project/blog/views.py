from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from blog.forms import BlogsListForm
from blog.models import Blog
from post.forms import PostsListForm
from post.models import Post


class BlogList(ListView):
    model = Blog
    template_name = "blog/blogs_list.html"
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super(BlogList, self).get_queryset()
        self.form = BlogsListForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['order_by']:
                queryset = queryset.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                queryset = queryset.filter(title__contains=self.form.cleaned_data['search'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['blogs_count'] = Blog.objects.all().count()
        context['form'] = self.form
        return context


class BlogDetail(ListView):
    model = Post
    template_name = "blog/blog_page.html"
    context_object_name = 'posts'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), id=kwargs.get('pk'))
        return super(BlogDetail, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(BlogDetail, self).get_queryset()
        self.form = PostsListForm(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['order_by']:
                queryset = queryset.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                queryset = queryset.filter(title__contains=self.form.cleaned_data['search'])
        return queryset.filter(blog=self.blog)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['form'] = self.form
        context['can_create'] = (
            self.request.user.id == self.blog.author.id
        )
        return context


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class NewBlog(CreateView):
    template_name = 'blog/new_blog.html'
    model = Blog
    fields = 'title', 'description', 'categories'

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewBlog, self).form_valid(form)
