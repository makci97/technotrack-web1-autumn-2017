from django import forms


class BlogsListForm(forms.Form):

    order_by = forms.ChoiceField(choices=(
        ('title', 'Title asc'),
        ('-title', 'Title desc'),
        ('id', 'Id asc'),
        ('-id', 'Id desc'),
    ), required=False)
    search = forms.CharField(required=False)
