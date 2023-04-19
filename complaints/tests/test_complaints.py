from faker import Faker
from django_test import TestCase


from complaints.models.complaint.models import Complaint as Master
from complaints.models.complaint.factories import ComplaintFactory as MasterFactory

fake = Faker()


class ComplaintTest(TestCase):
    def test_create_complaint(self):
        obj = MasterFactory.create()

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )