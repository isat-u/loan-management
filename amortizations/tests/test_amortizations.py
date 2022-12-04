from faker import Faker
from django_test import TestCase


from amortizations.models.amortization.models import Amortization as Master
from amortizations.models.amortization.factories import AmortizationFactory as MasterFactory

fake = Faker()


class AmortizationTest(TestCase):
    def test_create_amortization(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )