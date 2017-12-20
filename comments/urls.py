from django.conf.urls import url
from comments import views

urlpatterns = [
    url(r'^comments/(?P<post_id>\d+)/$', views.CommentsList.as_view(), name='comments_list'),
    url(r'^comments/(?P<post_id>\d+)/new_comment/$', views.NewComment.as_view(), name='new_comment'),

    url(r'^delete/$', views.delete_it, name='delete'),
]
