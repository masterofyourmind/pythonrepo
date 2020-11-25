from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("/",views.index, name='home'),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("logout/", views.logoutUser, name="logout"),
    path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("exams", views.exams, name="exams"),
    path("teams", views.teams, name="teams"),
    path("myuser", views.all_users, name="myuser"),
    path('<str:slug>', views.BlogDetailView, name="blogPost"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
