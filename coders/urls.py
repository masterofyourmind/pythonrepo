"""coders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from programmer import views
from django.conf.urls import url
from programmer.api import UserList

handler404 = 'programmer.views.custom_page_not_found_view'
handler500 = 'programmer.views.custom_error_view'
handler403 = 'programmer.views.custom_permission_denied_view'
handler400 = 'programmer.views.custom_bad_request_view'


urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('admin/', admin.site.urls),
    url(r'^api/users_list/$', UserList.as_view(), name='user_list'),
    path('', include('programmer.urls')),
]
