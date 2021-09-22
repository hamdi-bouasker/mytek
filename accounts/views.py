from accounts.models import Account
from accounts.forms import RegistrationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages, auth



def register(request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            # username = form.cleaned_data['email'].split('@')
            password = form.cleaned_data['password']
            user = Account.objects.create_user(f_name=f_name, l_name=l_name, email=email, password=password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please click the link below to activate your account.'
            message = render_to_string('accounts/register_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.fail_silently = False
            send_email.send()
            
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
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success('Your are logged out.')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render('accounts/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Please click the link below to reset your password.'
            message = render_to_string('accounts/password_reset_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'If your account exists, you will receive a reset password link shortly.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email address. Please check for typos and submit another password reset request.')
            return redirect('forgot_password')
    else:
        return render(request, 'accounts/forgotpassword.html')



