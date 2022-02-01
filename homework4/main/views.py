from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserPost
from django.contrib.auth.forms import UserCreationForm


def main_page(request):
    return render(request, 'index.html', {})


# TODO:
#   some links design
#   some page design
#   do cool templates for: create post, delete post, update post,
class PermissionToEditPostMixin(UserPassesTestMixin):
    def test_func(self):
        obj = super().get_object()
        return self.request.user.username == obj.created_by.username


class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'sign-up.html'
    success_url = '/'


class MainPage(ListView):
    model = UserPost
    fields = '__all__'
    template_name = 'textindex.html'
    ordering = 'created_at'


class PostPage(DetailView):
    model = UserPost
    template_name = 'single.html'


class ProfilePage(LoginRequiredMixin, ListView):
    model = UserPost
    fields = '__all__'
    template_name = 'profile.html'
    login_url = 'login/'
    ordering = 'created_at'

    def get_queryset(self):
        queryset = super(ProfilePage, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class CreatePost(LoginRequiredMixin, CreateView):
    model = UserPost
    fields = ['title', 'text']
    template_name = 'create_post.html'
    success_url = '/'
    login_url = '/profile/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(CreatePost, self).form_valid(form)


class UpdatePost(PermissionToEditPostMixin, UpdateView):
    model = UserPost
    fields = ['title', 'text']
    template_name = 'update_post.html'
    success_url = '/'
    login_url = '/profile/login/'


class DeletePost(PermissionToEditPostMixin, DeleteView):
    model = UserPost
    success_url = '/'
    login_url = '/profile/login/'
    template_name = 'delete_post.html'


class Logout(LogoutView):
    template_name = 'logout.html'
    redirect_field_name = '/'

