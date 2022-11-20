from faker import Faker
from django_test import TestCase


from loans.models.loan.models import Loan as Master
from loans.models.loan.factories import LoanFactory as MasterFactory

fake = Faker()


class LoanTest(TestCase):
    def test_create_loan(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )