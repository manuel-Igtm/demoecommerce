from django.utils import timezone
from .models import Shipping

def run():
    print("Seeding shipping...")

    Shipping.objects.all().delete()
    

   

    shippings = [
        Shipping.objects.create(order_id=1,  status="in_transit", tracking_number="TRACK123", estimated_delivery=timezone.now().date()),
        Shipping.objects.create(order_id=2,  status="pending", tracking_number="TRACK124", estimated_delivery=timezone.now().date()),
    ]

    print(f"Seeded {{{len(shippings)} shippings.")

if __name__ == "__main__":
    run()

