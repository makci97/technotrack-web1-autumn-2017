from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from comments.forms import CommentForm
from comments.models import Comment
from django.template.defaulttags import register
from django.http import JsonResponse, HttpResponse

from like.models import Like
from post.models import Post


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class CommentsList(ListView):
    model = Comment
    template_name = "comments/comments_list.html"
    context_object_name = 'comments'

    def dispatch(self, request, post_id=None, *args, **kwargs):
        self.post_id = post_id
        return super(CommentsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = super(CommentsList, self).get_queryset().filter(post_id=self.post_id)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(CommentsList, self).get_context_data(**kwargs)
        for comment in context['comments']:
            comment.create_like_fields(self.request.user)
        return context


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data, status=200)
        else:
            return response


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class NewComment(AjaxableResponseMixin, CreateView):
    template_name = 'comments/new_comment_dialog.html'
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, post_id=None, *args, **kwargs):
        self.post_id = post_id
        return super(NewComment, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewComment, self).get_context_data(**kwargs)
        context['post_id'] = self.post_id
        return context

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']
        # return reverse('post:post_detail', kwargs={'pk': self.post_id})

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.all().filter(id=self.post_id).first()
        return super(NewComment, self).form_valid(form)
