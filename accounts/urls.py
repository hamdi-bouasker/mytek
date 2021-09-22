from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('forgot_password/', views.forgot_password, name='forgot_password'),
]