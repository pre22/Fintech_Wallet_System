import random
import string
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from platform_wallet.managers import CustomUserManager


class CustomUser(AbstractUser):
    '''Custom User Model'''

    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=254)
    date_of_birth = models.DateField(
        _("date of birth"), max_length=150, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    verified = models.BooleanField(_("verified"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify("{}-{}-{}".format(self.first_name, self.last_name,
                            ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))))
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        return self.email


class Referals(models.Model):
    '''Referral Model'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    referred_user = models.CharField(max_length=200)
    referred_email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.slug


class NewsLetter(models.Model):
    subscriber = models.EmailField(max_length=254)

    def __str__(self):
        return self.subscriber
    
