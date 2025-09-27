from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Category

User = get_user_model()


DISCOUNT_TYPE = (
    ("percentage", "Percentage"),
    ("fixed", "Fixed Amount"),
)


class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE)
    value = models.DecimalField(max_digits=8, decimal_places=2)  # percentage or amount
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True, related_name="discounts")
    categories = models.ManyToManyField(Category, blank=True, related_name="discounts")
    users = models.ManyToManyField(User, blank=True, related_name="discounts")  # loyalty program

    def __str__(self):
        return f"{self.code} - {self.discount_type} ({self.value})"

