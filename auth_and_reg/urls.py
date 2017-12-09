from django.conf.urls import url
from auth_and_reg import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='auth_and_reg/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='auth_and_reg/logout.html'), name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
]