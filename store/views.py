from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        shipping_price = 20 # shipping price is set to $20 as exemple, it should be developed to calculate km or miles
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2*total)/100 # tax is set to 2% as exemple
        grand_total = total + tax + shipping_price
    except ObjectDoesNotExist:
        pass

    context = {
        "total":total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
        "shipping_price": shipping_price,
    }
        
    return render(request, 'store/checkout.html', context)
