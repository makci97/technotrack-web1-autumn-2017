from django.conf.urls import url
from blog import views
from post.views import NewPost, EditPost

urlpatterns = [
    url(r'^$', views.BlogList.as_view(), name='blog_list'),
    url(r'^blog_page/(?P<pk>\d+)$', views.BlogDetail.as_view(), name='blog_detail'),
    url(r'^blog_page/(?P<blog_id>\d+)/new_post$', NewPost.as_view(), name='new_post'),
    url(r'^blog_page/(?P<blog_id>\d+)/edit_post/(?P<pk>\d+)', EditPost.as_view(), name='edit_post'),
]
