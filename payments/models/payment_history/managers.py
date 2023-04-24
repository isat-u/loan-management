from django.db import models
from django.apps import apps
from django.conf import settings
from twilio.rest import Client


class PaymentHistoryQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class PaymentHistoryManager(models.Manager):
    def get_queryset(self):
        return PaymentHistoryQuerySet(self.model, using=self._db)
    
    def actives(self):
        return self.get_queryset().actives()

    def inactive(self):
        return self.get_queryset().inactive()
    
    def create(self, *args, **kwargs):
        try:
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'Hello {kwargs["account"]}, your payment request amounting {kwargs["amount"]} has been received. We will get back to you shortly.',
                from_=settings.FROM_NUMBER,
                to=kwargs["provider_data"]['contact_phone']
            )
            print(message.sid)
        except Exception as e:
            print('*****************************************************')
            print(e)
            print('*****************************************************')
        return super().create(*args, **kwargs)
