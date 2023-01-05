from faker import Faker
from django_test import TestCase


from payments.models.payment_request.models import PaymentRequest as Master
from payments.models.payment_request.factories import PaymentRequestFactory as MasterFactory

fake = Faker()


class PaymentRequestTest(TestCase):
    def test_create_payment_request(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )