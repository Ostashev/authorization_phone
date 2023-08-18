import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    verification_code = models.CharField(max_length=4, null=True)
    verified = models.BooleanField(default=False)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    activated_invite_code = models.CharField(
        max_length=6,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=200, null=True, unique=True)
    invited_users = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False
    )

    def generate_invite_code(self):
        return ''.join(random.choices(
            string.ascii_letters + string.digits, k=6
        ))

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.phone_number)
