from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.text import slugify
from django.template import loader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .constants import USER, ADMIN, SUPERADMIN


class AccountQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)

class AccountManager(BaseUserManager):
    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def create_user(self, username=None, password=None, email=None, user_type=USER, is_member=True):
        """
        Create base user
        :param email:
        :param username:
        :param password:
        :param user_type:
        :param parent:
        :return: Account or False
        """
        if email:
            email_validator = EmailValidator()
            try:
                email_validator(email)
                email = self.normalize_email(email)
            except ValidationError:
                pass

        user = self.model(
            username=username,
            email=email,
            user_type=user_type,
            is_member=is_member,
        )

        user.set_password(password)
        user.save(using=self._db)
        profile = user.profile
        subject = 'Maayon Loan Management System'
        context = {
            'site_name': "Loan Management System",
            'domain': settings.SITE_URL,
            'user': user,
            'password': password,
        }

        email_template = 'email/create_user_email.html'
        body = loader.render_to_string(email_template, context)
        
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=user.email,
            subject=subject,
            html_content=body,
        )
        
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        
        return user

    def create_superuser(self, username, password, email=None):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            user_type=SUPERADMIN
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
