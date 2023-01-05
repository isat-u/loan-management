import factory
from faker import Faker

from .models import PaymentRequest as Master

fake = Faker()


class PaymentRequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
