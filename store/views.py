from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        topSelling_products = Product.objects.filter(is_available=True, is_topSelling=True).order_by()[:3]
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)     
        topSelling_products = Product.objects.filter(is_available=True, is_topSelling=True).order_by()[:3]
        product_count = products.count()
    return render(request, 'store/store.html', {'products':paged_products, 'product_count': product_count, 'topSelling_products':topSelling_products})  

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    return render(request, 'store/product.html', {'single_product': single_product, 'in_cart': in_cart}) 

def search(request): 
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
    return render(request, 'store/store.html', {'products':products})