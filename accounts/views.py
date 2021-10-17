
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages, auth
from .models import Account, Profile
from.forms import RegistrationForm, UserForm, UserProfileForm 
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import Order, OrderProduct


def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            tel = form.cleaned_data['tel']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(f_name=f_name, l_name=l_name, email=email, tel=tel, password=password)
            user.save()

            current_site = get_current_site(request)
            subject = 'Account activation'
            body = render_to_string('accounts/register_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, body, to=[to_email])
            #send_email.fail_silently = False
            if send_email.send():
                return redirect('/accounts/login/?command=verification&email='+email)

        else:
            form = RegistrationForm()
            return render(request, 'accounts/register.html', {'form':form})
    else:
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link! Please try again.')
        return redirect('register')

def login(request):
    if request.method == 'POST': 
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                items_exists = CartItem.objects.filter(cart=cart).exists()
                if items_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Your are logged out.')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            subject = 'Password reset request.'
            body = render_to_string('accounts/password_reset_request.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, body, to=[to_email])
            send_email.send()
            messages.success(request, 'If your account exists, you will receive a reset password link shortly.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email address!')
            return redirect('forgot_password')
    else:
        return render(request, 'accounts/forgot_password.html')

def validate_reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Invalid activation link! Please try again.')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords did not match!')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')

@login_required
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    return render(request, 'accounts/my_orders.html', {'orders': orders})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':   
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is successfully updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            ok = user.check_password(current_password)
            if ok:
                user.set_password(confirm_password)
                user.save()
                #auth.logout(request)
                messages.success(request, 'Password successfully updated.')
                return redirect('change_password')
            else:
                messages.error(request, 'Wrong current password! Please retype it.')
                return render(request, 'accounts/change_password.html')
        else:
            messages.error(request, 'Passwords did not match! Please try again.')
            return render(request, 'accounts/change_password.html')

    return render(request, 'accounts/change_password.html')

@login_required
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for prod in order_detail:
        subtotal += round((prod.product_price * prod.quantity), 2)  
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)













