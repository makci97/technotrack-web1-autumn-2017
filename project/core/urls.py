from django.conf.urls import url
from core import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginView.as_view(template_name='core/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
]