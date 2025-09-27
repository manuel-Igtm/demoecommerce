from django.utils import timezone
from .models import Payment, User, Order


def run():
    print("Seeding payments...")

    # Ensure a user exists
    user, _ = User.objects.get_or_create(
        username="testuser",
        defaults={"email": "test@example.com"}
    )

    # Ensure an order exists
    order, _ = Order.objects.get_or_create(
        id=1,
        defaults={
            "created_by": user,    # use created_by instead of user
            "total": 500.0,        # use total instead of total_price
            "status": "pending"
        }
    )

    Payment.objects.all().delete()

    payments = [
        Payment.objects.create(
            user=user,                # ✅ pass user
            order=order,              # ✅ pass order object instead of order_id
            amount=500.0,
            provider="chapa",
            transaction_id="chapa_txn_001",
            status="completed",
            created_at=timezone.now()
        ),
        Payment.objects.create(
            user=user,
            order=order,
            amount=1200.0,
            provider="chapa",
            transaction_id="chapa_txn_002",
            status="pending",
            created_at=timezone.now()
        ),
    ]

    print(f"Seeded {len(payments)} payments.")


if __name__ == "__main__":
    run()
