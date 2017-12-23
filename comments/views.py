from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db import models

from comments.forms import CommentForm
from comments.models import Comment
from django.http import JsonResponse, HttpResponse

from like.models import Like
from post.models import Post


class CommentsList(ListView):
    model = Comment
    template_name = "comments/comments_list.html"
    context_object_name = 'comments'

    def dispatch(self, request, post_id=None, *args, **kwargs):
        self.post_id = post_id
        # for comment in Comment.objects.all():
        #     comment.create_like_fields(self.request.user)
        #     Comment.objects.filter(id=comment.id).update(likes_count=comment.likes_count)
        return super(CommentsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = super(CommentsList, self).get_queryset().filter(
            models.Q(post_id=self.post_id) & (
            models.Q(is_deleted=False) | models.Q(post__author_id=self.request.user.id))
        ).annotate(
            # likes_count=models.Sum(
            #     models.Case(
            #         models.When(likes__liked=True, then=1),
            #         default=0, output_field=models.IntegerField()
            #     )
            # ),
            is_liked=models.Sum(
                models.Case(
                    models.When(likes__liked=True, likes__user_id=self.request.user.id, then=1),
                    default=0, output_field=models.IntegerField()
                ), output_field=models.BooleanField()
            ),
            is_invisible=models.Case(
                models.When(models.Q(is_deleted=True) & models.Q(post__author_id=self.request.user.id), then=True),
                default=False, output_field=models.BooleanField()
            )
        )

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(CommentsList, self).get_context_data(**kwargs)
        # for comment in context['comments']:
        #     comment.create_like_fields(self.request.user)
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


def delete_it(request):
    user = request.user
    if request.method == 'POST':
        object_id = int(request.POST['object_id'])
        content_type_name = str(request.POST['content_type'])

        if content_type_name == 'Comment':
            obj = Comment.objects.filter(pk=object_id).first()
            return delete_comment(request, obj, user)

    return HttpResponse(content="Can't delete", status=500)


def delete_comment(request, obj, user):
    comment = obj
    if comment.post.author.id == user.id:
        comment.change_is_deleted()
        context = {'comment':
            Comment.objects.filter(id=comment.id).filter(
                models.Q(post_id=comment.post.id) & (models.Q(is_deleted=False) | models.Q(post__author_id=user.id))
            ).annotate(
                # likes_count=models.Sum(
                #     models.Case(
                #         models.When(likes__liked=True, then=1),
                #         default=0, output_field=models.IntegerField()
                #     )
                # ),
                is_liked=models.Sum(
                    models.Case(
                        models.When(likes__liked=True, likes__user_id=user.id, then=1),
                        default=0, output_field=models.IntegerField()
                    ), output_field=models.BooleanField()
                ),
                is_invisible=models.Case(
                    models.When(models.Q(is_deleted=True) & models.Q(post__author_id=user.id), then=True),
                    default=False, output_field=models.BooleanField()
                )
            ).first()
        }

        return render(request, 'comments/comment.html', context)

    return HttpResponse(content="Can't delete", status=404)
