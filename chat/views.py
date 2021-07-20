from django.shortcuts import render, reverse, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

User = get_user_model()


class Login(LoginView):
    def get_success_url(self):
        return reverse('room', args=[self.request.user.username])


def room(request, username):
    if request.user.username != username:
        if not request.user.is_authenticated:
            return redirect('login')
        return redirect(f'/chat/{request.user.username}')
    context = {
        'username': username,
        'users': User.objects.exclude(username=username)
    }
    return render(request, 'chat/room.html', context)