from django.conf.urls import url
from like import views

urlpatterns = [
    url(r'^$', views.like_it, name='like'),
    # url(r'^new_blog/$', views.NewBlog.as_view(), name='new_blog'),
    # url(r'^blog_page/(?P<pk>\d+)/$', views.BlogDetail.as_view(), name='blog_detail'),
    # url(r'^blog_page/(?P<blog_id>\d+)/new_post/$', NewPost.as_view(), name='new_post'),
]
