from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(CommentForm, self).clean()
        if self.user is None or self.user.is_anonymous():
            raise forms.ValidationError(u'Вы не можете опубликовать комментарий, пока не авторизуетесь')
        return data

    class Meta:
        model = Comment
        fields = ('text', )
