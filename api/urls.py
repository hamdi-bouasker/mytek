from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('reviews/', views.ReviewRatingList.as_view()),
    path('orders-products/', views.OrderProductList.as_view()),
]