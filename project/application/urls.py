"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('auth_and_reg.urls', namespace="auth")),
    url(r'^blogs/', include('blog.urls', namespace="blog")),
    url(r'^comments/', include('comments.urls', namespace="comments")),
    url(r'^likes/', include('like.urls', namespace="like")),
    url(r'^', include('core.urls', namespace="core")),
    url(r'^posts/', include('post.urls', namespace="post")),
]

if settings.DEBUG is True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)