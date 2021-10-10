from rest_framework import serializers
from category.models import Category
from store.models import Product, ReviewRating
from orders.models import OrderProduct


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['category', 'name', 'brand_name', 'slug', 'description', 'price', 'product_image', 'discount_percentage', 'product_image', 'alt_text', 'stock', 'is_available', 'is_trending', 'is_topSelling', 'logo_image', 'logo_altText', 'created_at', 'updated_at', 'discount_price']
    

class ReviewRatingSerializer(serializers.ModelSerializer):

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = ReviewRating
        fields = ['product', 'user', 'subject', 'review', 'rating', 'ip', 'status', 'created_at', 'updated_at']


class OrderProductSerializer(serializers.ModelSerializer):

    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    payment = serializers.StringRelatedField()

    class Meta:
        model = OrderProduct
        fields = ['order', 'payment', 'user', 'product', 'quantity', 'product_price', 'ordered', 'created_at', 'updated_at']