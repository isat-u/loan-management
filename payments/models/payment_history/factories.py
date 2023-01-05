import factory
from faker import Faker

from .models import PaymentHistory as Master

fake = Faker()


class PaymentHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
