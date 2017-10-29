from django.shortcuts import reverse, get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView

from blog.models import Blog
from comments.forms import CommentForm
from post.models import Post


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.all(), id=pk)
    context = {'post': post}
    if request.method == 'POST':
        print(request.user)
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post:post_detail', pk=pk)
    else:
        form = CommentForm(user=request.user)
    context['form'] = form
    context['can_edit'] = (
        request.user.id == post.blog.author.id == post.author.id
    )
    return render(request, 'post/post_page.html', context)


# class PostDetail(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'post/post_page.html'
#     context_object_name = 'comment'
#     fields = 'text'
#
#     post = models.ForeignKey(Post, related_name='comments')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL)
#
#     def dispatch(self, request, *args, **kwargs):
#         self.post = get_object_or_404(Post.objects.all(), id=kwargs.get('pk'))
#         return super(PostDetail, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data(**kwargs)
#         context['can_edit'] = (
#             self.request.user.id == self.object.blog.author.id == self.object.author.id
#         )
#         context['post'] = self.post
#         return context
#
#     form.is_valid()
#
#     # def get_success_url(self):
#     #     return reverse('post:post_detail', kwargs={'pk': self.object.pk})
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.blog = self.blog
#         return super(NewPost, self).form_valid(form)


class NewPost(CreateView): #, UserPassesTestMixin):
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
        if not self.test_func():
            return redirect('blog:blog_detail', pk=blog_id)
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


class EditPost(UpdateView): #, UserPassesTestMixin):
    template_name = 'post/edit_post.html'
    model = Post
    fields = 'title', 'text', 'categories'


    def test_func(self):
        return self.can_edit

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        # print(EditPost.mro())
        self.blog = get_object_or_404(Blog.objects.all(), id=blog_id)
        self.can_edit = (
            self.request.user.id == self.blog.author.id == self.object.author.id
        )
        if not self.test_func():
            return redirect('post:post_detail', pk=kwargs.get('pk'))
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
