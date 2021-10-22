from django.db import models

class Subscribe(models.Model):
    email = models.EmailField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    email = models.EmailField(max_length=150)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
