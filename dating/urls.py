from django.urls import path,re_path
from . import views

from django.contrib.auth import views as auth_views
from .views import ThreadView


urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    
    
    path('editprofile/', views.profile, name='editprofile'),
    path('profile/', views.prof, name='profile'),

    path('messages/', views.Messagepage, name='Message'),
    path("messages/<username>/", ThreadView.as_view()),
    path('', views.homepage, name='home'),
    path('explore/', views.searchpage, name='explore'),
    path('user_settings', views.userSettings, name='user_settings'),
    path('update_theme', views.updattheme, name='update_theme'),




    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='dating/password_reset.html'),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='dating/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='dating/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view() ,name="password_reset_complete"),

    
    
    
]

