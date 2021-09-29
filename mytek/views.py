from django.shortcuts import render
from store.models import Product, ReviewRating

def index(request):
    
    products = Product.objects.all().filter(is_available=True, is_trending=True)
    # for product in products:
    #     review = ReviewRating.objects.filter(product_id = product.id, status=True)
   
    return render(request, 'index.html', {'products':products})
