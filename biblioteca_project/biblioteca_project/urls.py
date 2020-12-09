# Project urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', usuarios_views.register, name='registro'),
    path('profile/', usuarios_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path('gerenciamento/', include('gerenciamento.urls')),
    path('', include('gerenciamento.urls')),
]
