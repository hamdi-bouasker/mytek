from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    if user.is_authenticated:
        try:
            cart_item =CartItem.objects.get(product=product, user = user)
            cart_item.quantity +=1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = user,
            )
            cart_item.save()
    
        return redirect('cart')

    else:

        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()

        try:
            cart_item =CartItem.objects.get(product=product, cart = cart)
            cart_item.quantity +=1
            cart_item.save()
            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
    
        return redirect('cart')

def remove_cart(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(user=user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            
        return redirect('cart')

def remove_cart_item(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            if item.product.discount_price:
                total += (item.product.discount_price * item.quantity)
                quantity += item.quantity
            else:
                total += (item.product.price * item.quantity)
                quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = tax + total 

    except ObjectDoesNotExist:
        pass

    context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
        }

    return render(request, 'store/cart.html', context)