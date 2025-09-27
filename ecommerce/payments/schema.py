import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone
from .models import Payment, Order


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ("id", "order", "amount", "provider", "transaction_id", "status", "created_at")


class Query(graphene.ObjectType):
    all_payments = graphene.List(PaymentType)
    payment = graphene.Field(PaymentType, id=graphene.ID(required=True))

    def resolve_all_payments(root, info):
        return Payment.objects.select_related("order").all()

    def resolve_payment(root, info, id):
        return Payment.objects.get(pk=id)


class CreatePayment(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        amount = graphene.Float(required=True)
        provider = graphene.String(required=True)

    payment = graphene.Field(PaymentType)

    def mutate(self, info, order_id, amount, provider):
        order = Order.objects.get(pk=order_id)
        payment = Payment.objects.create(
            order=order,
            amount=amount,
            provider=provider,
            transaction_id=f"{provider}_txn_{timezone.now().timestamp()}",
            status="pending",
            created_at=timezone.now(),
        )
        return CreatePayment(payment=payment)


class Mutation(graphene.ObjectType):
    create_payment = CreatePayment.Field()
