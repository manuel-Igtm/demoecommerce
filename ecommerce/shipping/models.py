from django.db import models
from orders.models import Order


SHIPPING_STATUS = (
    ("pending", "Pending"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipping")
    provider = models.CharField(max_length=100, default="Local Courier")
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SHIPPING_STATUS, default="pending")
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)  # hybrid option

    def __str__(self):
        return f"{self.order} - {self.status}"
