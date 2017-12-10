from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.files.images import get_image_dimensions


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    avatar = forms.ImageField(required=False, help_text='Optional')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar is None:
            return avatar
        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 2700
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (40 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 40k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'avatar', 'password1', 'password2', )