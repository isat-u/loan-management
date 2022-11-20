import factory
from faker import Faker

from .models import LoanType as Master

fake = Faker()


class LoanTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
