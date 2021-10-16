from django.http import JsonResponse
from store.models import Product
from django.shortcuts import render, redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime
from django.contrib import messages
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count < 1:
        return redirect('store')

    grand_total = 0
    tax = 0
    total = 0
    shipping_price = 20 # to be developped to calculate shipping price on distance basis
    for item in cart_items:
            if item.product.discount_price:
                total += round(((item.product.discount_price) * item.quantity), 2)
                quantity += item.quantity
            else:
                total += round(((item.product.price) * item.quantity), 2)
                quantity += item.quantity

    tax = round(((2 * total) / 100), 2)
    grand_total = round((tax + total + shipping_price), 2) 
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.f_name = form.cleaned_data['f_name']
            data.l_name = form.cleaned_data['l_name']
            data.email = form.cleaned_data['email']
            data.tel = form.cleaned_data['tel']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zipcode = form.cleaned_data['zipcode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            if request.POST.get('terms', None) == None:             
                messages.error(request, 'You must accept terms & conditions! Please go back to cart and restart checkout process.')
                return render(request, 'store/checkout.html')
            else:
                data.save()

            year = int(datetime.date.today().strftime('%Y'))
            month = int(datetime.date.today().strftime('%m'))
            day = int(datetime.date.today().strftime('%d'))
            d = datetime.date(year, month, day)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'shipping_price': shipping_price,
                'grand_total': grand_total
            }

            return render(request, 'orders/payment.html', context)

        else:
            messages.error(request, 'Invalid inputs!')
            return redirect('checkout')

def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transactionID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    subject = 'Account activation'
    body = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(subject, body, to=[to_email])

    data = {
        'order_number': order.order_number,
        'transactionID': payment.payment_id
    }

    return JsonResponse(data)

def order_completed(request):
    order_number = request.GET.get('order_number')
    transactionID = request.GET.get('payment_id')
    payment = Payment.objects.get(payment_id=transactionID)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for prod in ordered_products:
            subtotal += (prod.product_price * prod.quantity)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'ordder_number': order.order_number,
            'transactionID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_completed.html', context)
        
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('index')
    
