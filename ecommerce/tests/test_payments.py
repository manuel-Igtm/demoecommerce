import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from orders.models import Order
from users.models import User
from payments.models import Payment


@pytest.mark.django_db
class TestPayments:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="buyer", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(user=self.user, total=500)

        self.payment_url = reverse("payment-initiate")   # adjust to your URL
        self.verify_url = reverse("payment-verify", args=[self.order.id])

    def test_initiate_payment(self):
        payload = {"order_id": self.order.id, "method": "mpesa"}
        response = self.client.post(self.payment_url, payload, format="json")
        assert response.status_code == 200
        assert "payment_id" in response.data
        assert response.data["status"] == "PENDING"

    def test_payment_verification_success(self):
        payment = Payment.objects.create(order=self.order, amount=500, status="PENDING")

        # Simulate API callback or polling
        response = self.client.post(self.verify_url, {"payment_id": payment.id, "status": "SUCCESS"}, format="json")
        assert response.status_code == 200
        payment.refresh_from_db()
        assert payment.status == "SUCCESS"
        assert self.order.status == "PAID"

    def test_payment_verification_failed(self):
        payment = Payment.objects.create(order=self.order, amount=500, status="PENDING")

        response = self.client.post(self.verify_url, {"payment_id": payment.id, "status": "FAILED"}, format="json")
        assert response.status_code == 400
        payment.refresh_from_db()
        assert payment.status == "FAILED"
