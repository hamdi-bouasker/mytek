from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('forgot_password/', views.forgot_password, name='forgot_password'),
  path('validate_reset_password/<uidb64>/<token>/', views.validate_reset_password, name='validate_reset_password'),
  path('reset_password/', views.reset_password, name='reset_password'),
  path('my_orders/', views.my_orders, name='my_orders'),
  path('edit_profile/', views.edit_profile, name='edit_profile'),
  path('change_password/', views.change_password, name='change_password'),
  path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]