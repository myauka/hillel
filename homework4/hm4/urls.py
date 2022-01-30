"""hm4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
import django.contrib.auth.views as auth_views
from main.views import UserRegistrationView, MainPage, CreatePost, \
    UpdatePost, DeletePost, ProfilePage, Logout, PostPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('profile/', ProfilePage.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('profile/login/', auth_views.LoginView.as_view(template_name='sign-in.html')),
    path('profile/create_post/', CreatePost.as_view()),
    path('update_post/<slug:slug>/', UpdatePost.as_view(), name='user_post_detail'),
    path('delete/<slug:slug>/<pk>/', DeletePost.as_view()),
    path('profile/logout/', Logout.as_view()),
    path('post/<slug:slug>/', PostPage.as_view()),

]
