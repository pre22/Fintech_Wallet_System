import random
import string
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from platform_wallet.managers import CustomUserManager
from django.utils.text import slugify


class CustomUser(AbstractUser):

    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField(_("date of birth"), max_length=150, blank=False)
    verified = models.BooleanField(_("verified"), default=False)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify("{}-{}-{}".format(self.first_name, self.last_name,
                            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))))
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        return self.email
