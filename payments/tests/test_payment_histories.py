from faker import Faker
from django_test import TestCase


from payments.models.payment_history.models import PaymentHistory as Master
from payments.models.payment_history.factories import PaymentHistoryFactory as MasterFactory

fake = Faker()


class PaymentHistoryTest(TestCase):
    def test_create_payment_history(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )