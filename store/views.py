from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import OrderProduct
from .forms import ReviewForm
from .models import Product, ProductGallery, ReviewRating
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    try:
        orderproduct = OrderProduct.objects.filter(user=request.user.id, product_id = single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)
    reviews_count = reviews.count()
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)

    context = {
        'single_product': single_product, 
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'reviews_count': reviews_count,
        'product_gallery': product_gallery,
    }
    
    return render(request, 'store/product.html', context) 

def search(request): 
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
    return render(request, 'store/store.html', {'products':products})


@login_required
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
            total += round((item.product.price * item.quantity), 2)
            quantity += item.quantity
        tax = round(((2*total)/100),2) # tax is set to 2% as exemple
        grand_total = round((total + tax + shipping_price), 2)
        
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            # updated_at
            form.save()
            messages.success(request, 'Review updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                # created_at
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Review created.')
                return redirect(url)





