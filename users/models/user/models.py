from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=42, blank=True, null=True)
    middle_name = models.CharField(max_length=42, blank=True, null=True)
    last_name = models.CharField(max_length=42, blank=True, null=True)
    gender = models.ForeignKey(
        'profiles.Gender',
        null=True,
        db_index=False,
        on_delete=models.SET_NULL,
        related_name='users_gender'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
