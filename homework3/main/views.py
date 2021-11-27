import random
import secrets
import string
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
from main.models import UrlFromUser


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UrlFromUser
        fields = ['link']


def generate_link_id():
    alphabet = string.ascii_letters + string.digits
    size = random.randint(5, 6)
    link_id = ''.join(secrets.choice(alphabet) for _ in range(size))
    return link_id


def main_page(request):
    return render(request, 'index.html', {})


def registration(request):
    form = UserCreationForm(request.POST or None)
    if form.is_bound and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'register.html', {'form': form})


@login_required
def profile_handler(request):
    form = ProfileForm(request.POST or None)
    content = {}
    if form.is_bound and form.is_valid():
        data = form.save(commit=False)
        data.short_url = generate_link_id()
        data.save()
        content['short_url'] = data.short_url
    content['form'] = form
    return render(request, 'profile.html', content)


def redirect_by_id(request, link_id):
    url = UrlFromUser.objects.get(short_url=link_id)
    url.redirect_count += 1
    url.save()
    return redirect(url.link)
