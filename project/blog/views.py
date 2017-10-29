from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from blog.models import Blog
from post.forms import PostsListForm
from post.models import Post


class BlogList(ListView):
    model = Blog
    template_name = "blog/blogs_list.html"
    context_object_name = 'blogs'
    paginate_by = 1


class BlogDetail(ListView):
    model = Post
    template_name = "blog/blog_page.html"
    context_object_name = 'posts'
    paginate_by = 2

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
                queryset = queryset.filter(title=self.form.cleaned_data['search'])
        return queryset.filter(blog=self.blog)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['form'] = self.form
        context['can_create'] = (
            self.request.user.id == self.blog.author.id
        )
        return context


# class BlogDetail(DetailView):
#     model = Blog
#     template_name = "blog/blog_page.html"
#     context_object_name = 'blog'
#     paginate_by = 2
#
#     def get_context_data(self, **kwargs):
#         context = super(BlogDetail, self).get_context_data(**kwargs)
#         context['can_create'] = (
#             self.request.user.id == self.object.author.id
#         )
#         return context
#
#     def get_object(self, queryset=None):
#         if queryset is None:
#             queryset = super(BlogDetail, self).get_queryset()
#         return super(BlogDetail, self).get_object(queryset)
#
#     def get_queryset(self):
#         # return Post.objects.all()
#         print(self.object)
#         return self.object.posts.all()
