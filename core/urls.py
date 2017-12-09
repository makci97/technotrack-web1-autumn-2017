from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^user/(?P<pk>\d+)/posts$', views.UserPostsList.as_view(), name='user_posts_list'),
    url(r'^user/(?P<pk>\d+)/blogs$', views.UserBlogsList.as_view(), name='user_blogs_list'),
    url(r'^user/(?P<pk>\d+)/edit$', views.UserEdit.as_view(), name='edit_user'),
    url(r'^category/new$', views.NewCategory.as_view(), name='new_category'),
]
