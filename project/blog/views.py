from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from blog.models import Blog


class BlogList(ListView):
    template_name = "blog/blogs_list.html"
    context_object_name = 'blogs'
    model = Blog


class BlogDetail(DetailView):
    template_name = "blog/blog_page.html"
    context_object_name = 'blog'
    model = Blog
