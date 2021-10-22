from django.shortcuts import render, redirect
from .forms import SubscribeForm, ContactForm
from django.contrib import messages


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Successful.')
            return redirect('index')
                
        else:
            messages.error(request, 'You are already subscribed!')
            return render(request, 'index.html', {'form':form})        
    else:
        form = SubscribeForm()
        return render(request, 'index.html', {'form':form})


def contact_me(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()          
            messages.success(request, 'Message has been sent. Thank you for contacting us.')
            return redirect('index')
            
        else:
            form = ContactForm()
            messages.error(request, 'Message not sent! Please try again later.')
            return render(request, 'index.html', {'form':form})
    else:
        form = ContactForm()
        return render(request, 'index.html', {'form':form})
