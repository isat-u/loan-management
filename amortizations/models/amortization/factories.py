import factory
from faker import Faker

from .models import Amortization as Master

fake = Faker()


class AmortizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
