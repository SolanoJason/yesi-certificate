from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login')
]

