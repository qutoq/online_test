from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('test/<int:id>', views.test_view, name='test_view'),
    path('test/<int:id>/result', views.result_view, name='result'),

    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-then-login', auth_views.logout_then_login, name='logout_then_login'),
    path('register', views.register, name='register'),
    path('password_change', views.password_change, name="password_change"),
    path('profile', views.profile, name='profile'),
]

app_name = 'app'
