import factory
from faker import Faker

from .models import Complaint as Master

fake = Faker()


class ComplaintFactory(factory.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
    name = factory.LazyAttribute(lambda x: fake.name())
