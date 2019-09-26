from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

# Create your models here.


class MainUserProfile(models.Model):
    PACKAGE_CHOICES = (
        ('1', "Basic"),
        ('2', "Standard"),
        ('3', "Premium")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="main_user_profile")
    address = models.TextField()
    phone_number = models.CharField(max_length=55)
    birthday = models.DateField()

    _package = models.CharField(choices=PACKAGE_CHOICES, max_length=55)
    _added = models.DateTimeField(auto_now_add=True)
    _updated = models.DateTimeField(auto_now=True)
    _blocked = models.BooleanField(default=False)

    objects = models.QuerySet()

    def __str__(self):
        return self.user.username


class ApplicationMonthlyPayment(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name="monthly_payments")
    _paid_time = models.DateTimeField()
    _next_pay = models.DateTimeField()

    objects = models.QuerySet()

    def __str__(self):
        return self.main_user


class Payment:

    def __init__(self, user_model):
        self.main_user = MainUserProfile.objects.get(user=user_model)

    def _get_last_payment_date(self):
        return ApplicationMonthlyPayment.objects.filter(main_user=self.main_user).\
            only("_paid_time").order_by("-_paid_time")[0]

    def _is_paid(self):
        return self._get_last_payment_date() > datetime.date.today()

    def __str__(self):
        return self.main_user


class SubUserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sub_user_profile")
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name="sub_user_profile")

    address = models.TextField()
    phone_number = models.CharField(max_length=55)
    birthday = models.DateField()

    _added = models.DateTimeField(auto_now_add=True)
    _updated = models.DateTimeField(auto_now=True)
    _blocked = models.BooleanField(default=False)

    objects = models.QuerySet()

    def __str__(self):
        return self.user.username


class Permission(models.Model):

    """Individual Permissions"""
    user = models.OneToOneField(SubUserProfile, on_delete=models.CASCADE, related_name="sub_user_permission")
    # Inventory
    inventory_see = models.BooleanField(default=False)
    inventory_add = models.BooleanField(default=False)
    inventory_mod = models.BooleanField(default=False)

    # To be continued...

    objects = models.QuerySet()

    def __str__(self):
        return self.user.user.username

