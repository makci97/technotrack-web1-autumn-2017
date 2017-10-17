from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from post.models import Post



class PostDetail(DetailView):
    template_name = 'post/post_page.html'
    context_object_name = 'post'
    model = Post
#
# def post_page(request, id):
#     post = get_object_or_404(Post.objects, id=id)
#     context = {'post': post}
#     return render(request, 'post/post_page.html', context)
