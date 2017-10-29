from django.conf.urls import url
from post import views

urlpatterns = [
    url(r'^post_page/(?P<pk>\d+)$', views.post_detail, name='post_detail'),
]
