from django.shortcuts import render, redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment
import datetime
from django.contrib import messages
import json

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count < 1:
        return redirect('store')

    grand_total = 0
    tax = 0
    shipping_price = 20 # to be developped to calculate shipping price on distance basis
    for item in cart_items:
            if item.product.discount_price:
                total += (item.product.discount_price * item.quantity)
                quantity += item.quantity
            else:
                total += (item.product.price * item.quantity)
                quantity += item.quantity

    tax = (2 * total) / 100
    grand_total = tax + total 
    
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
    return render(request, 'orders/payment.html')