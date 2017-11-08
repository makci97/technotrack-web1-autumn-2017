from django.conf.urls import url
from blog import views
from post.views import NewPost

urlpatterns = [
    url(r'^$', views.BlogList.as_view(), name='blog_list'),
    url(r'^new_blog/$', views.NewBlog.as_view(), name='new_blog'),
    url(r'^blog_page/(?P<pk>\d+)/$', views.BlogDetail.as_view(), name='blog_detail'),
    url(r'^blog_page/(?P<blog_id>\d+)/new_post/$', NewPost.as_view(), name='new_post'),
]
