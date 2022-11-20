from faker import Faker
from django_test import TestCase


from loans.models.loan_type.models import LoanType as Master
from loans.models.loan_type.factories import LoanTypeFactory as MasterFactory

fake = Faker()


class LoanTypeTest(TestCase):
    def test_create_loan_type(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )