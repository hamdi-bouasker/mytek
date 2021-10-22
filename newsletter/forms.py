from django import forms
from . models import Subscribe, Contact


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email', ]

    def clean(self):
        email = self.cleaned_data['email']
        if Subscribe.objects.filter(email=email).exists():
            raise forms.ValidationError('You are already subscribed!')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'title', 'body']