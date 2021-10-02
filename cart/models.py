from django.db import models
from store.models import Product
from accounts.models import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        if self.product.discount_price:
                theprice = self.product.discount_price * self.quantity
                return round(theprice, 2)
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product}"

