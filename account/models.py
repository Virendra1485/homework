from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser):
    RoleChoice = [
        ("CUSTOMER", "CUSTOMER"),
        ("WORKER", "WORKER")
    ]

    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    BLOCKER = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Ironing', 'Ironing'),
    ]

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    qr_picture = models.ImageField(upload_to='qr_picture/', null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    working_days = MultiSelectField(choices=DAY_CHOICES, validators=[MaxValueValidator(6)], default=[])
    role = models.CharField(max_length=20, choices=RoleChoice, default="WORKER")

    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions")
    amount = models.PositiveIntegerField(default=100)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    location_country = models.CharField(max_length=100, default="")
    location_city = models.CharField(max_length=100, default="")
    location_address = models.CharField(max_length=100, default="")
    blocker = MultiSelectField(choices=BLOCKER, validators=[MaxValueValidator(3)], default=[])
    stripe_customer_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


class Payment(models.Model):

    PAYMENT_STATUS_CHOICE = [
        ('REQUIRE_PAYMENT_METHOD', 'requires_payment_method'),
        ('REQUIRES_ACTION', 'requires_action'),
        ('SUCCEEDED', 'succeeded'),
        ('FAILED', 'Failed'),
    ]
    payment_id = models.CharField(max_length=50, unique=True, default="")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICE, default="requires_payment_method")
    payment_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="payment")
    paid_location_city = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
