from django.utils import timezone
from .models import Discount

def run():
    print("Seeding discounts...")

    Discount.objects.all().delete()

    discounts = [
        Discount.objects.create(code="WELCOME10", discount_type="percentage", value=10, active=True, valid_until=timezone.now().date()),
        Discount.objects.create(code="FREESHIP", discount_type="fixed", value=200, active=True, valid_until=timezone.now().date()),
    ]

    print(f"Seeded {len(discounts)} discounts.")


if __name__ == "__main__":
    run()
