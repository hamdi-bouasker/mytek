
from rest_framework import generics, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import CategorySerializer, ProductSerializer, ReviewRatingSerializer, OrderProductSerializer
from store.models import Product, ReviewRating
from orders.models import OrderProduct

class CategorySerializerList(generics.ListAPIView):
    serializer_class = CategorySerializer
    fields = ('name', 'slug', 'is_active')

class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    category = CategorySerializer()
    filter_fields = ('stock', 'is_available', 'is_trending', 'is_topSelling', 'created_at', 'updated_at')
    search_fields = ('^name', '^category__name',)

    @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

class ReviewRatingList(generics.ListAPIView):
    queryset = ReviewRating.objects.filter(status=True)
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('product', 'user', 'subject', 'review', 'rating', 'ip', 'status', 'created_at', 'updated_at')
    search_fields = ('^user__email', '^product__name',)

    @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

class OrderProductList(generics.ListAPIView):

    queryset = OrderProduct.objects.filter(ordered=True)
    serializer_class = OrderProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('order', 'payment', 'user', 'product', 'quantity', 'product_price', 'ordered', 'created_at', 'updated_at')
    search_fields = ('^payment__payment_id',)

    @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)