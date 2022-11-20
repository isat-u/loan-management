import factory
from faker import Faker

from .models import Loan as Master

fake = Faker()


class LoanFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
