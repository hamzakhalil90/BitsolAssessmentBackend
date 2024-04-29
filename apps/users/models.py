from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.baselayer.basemodels import LogsMixin
from User_Management_Backend.settings import AUTH_USER_MODEL
from apps.baselayer.utils import generate_access_token
import uuid


class Address(LogsMixin):
    """
        Model for storing Addresses
        """
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"


class Organization(LogsMixin):
    """
    Model for storing Organizations
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser, LogsMixin):
    """
        Model for storing Users
        """
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users", null=True,
                                     blank=True)
    addresses = models.ManyToManyField(Address, null=True, blank=True, related_name="users")

    def __str__(self):
        return self.name

    def get_access_token(self):
        return generate_access_token(self)


class Token(LogsMixin):
    user = models.ForeignKey(
        AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE, related_name="token"
    )
    token = models.TextField(max_length=500, unique=True, null=False, blank=False)
