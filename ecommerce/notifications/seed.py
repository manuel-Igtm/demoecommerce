from django.utils import timezone
from .models import Notification

def run():
    print("Seeding notifications...")

    Notification.objects.all().delete()

    notifications = [
        Notification.objects.create(user_id=1, message="Your order has been shipped!", notification_type="order", is_read=False, created_at=timezone.now()),
        Notification.objects.create(user_id=2, message="Payment received successfully.", notification_type="payment", is_read=True, created_at=timezone.now()),
    ]

    print(f"Seeded {len(notifications)} notifications.")

if __name__ == "__main__":
    run()

