from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, update_session_auth_hash,logout
from django.views.generic import (
    View
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

UserModel = get_user_model()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_account = form.save()
            return redirect('users:login')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse_lazy('users:login'))