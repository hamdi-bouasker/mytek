from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def store(request, category_slug=None):
    categories = None
    trending_products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by()[:12]
        topSelling_products = Product.objects.filter(is_available=True, is_topSelling=True).order_by()[:3]
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by()[:12]
        topSelling_products = Product.objects.filter(is_available=True, is_topSelling=True).order_by()[:3]
        product_count = products.count()
    return render(request, 'store/store.html', {'products':products, 'product_count': product_count, 'topSelling_products':topSelling_products})  

def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'store/product.html', {'single_product': single_product})  