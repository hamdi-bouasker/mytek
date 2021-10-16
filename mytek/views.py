from django.shortcuts import render
from django.views.decorators.cache import cache_page
from store.models import Product

@cache_page(60 * 15)
def index(request):
    products = Product.objects.all().filter(is_available=True, is_trending=True) 
    return render(request, 'index.html', {'products':products})
