from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.BlogList.as_view(), name='blog_list'),
    url(r'^blog_page/(?P<pk>\d+)$', views.BlogDetail.as_view(), name='blog_detail'),
]
