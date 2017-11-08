from django.conf.urls import url
from post import views

urlpatterns = [
    url(r'^post_page/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^edit_post/(?P<pk>\d+)/$', views.EditPost.as_view(), name='edit_post'),
]
