from django.db import models
from django.utils.timezone import now
from profile_app.models import MainUserProfile


# Create your models here.


class InventoryFoodName(models.Model):
    UNIT_CHOICES = (
        ('kg', 'KG'),
        ('ltr', 'LTR'),
        ('pcs', 'PCS')
    )
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_food_names')

    name = models.CharField(max_length=255)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=5)

    objects = models.QuerySet()

    def __str__(self):
        return self.name


class InventoryFoodIN(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_foods_in')

    name = models.ForeignKey(InventoryFoodName, on_delete=models.CASCADE, related_name='inventory_foods_in')
    quantity = models.FloatField()

    price = models.FloatField()
    date = models.DateField(default=now)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.QuerySet()

    def __str__(self):
        return self.name.__str__()


class InventoryFoodOUT(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_foods_out')

    name = models.ForeignKey(InventoryFoodIN, on_delete=models.CASCADE, related_name='inventory_foods_out')
    quantity = models.FloatField()
    date = models.DateField(default=now)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.QuerySet()

    def __str__(self):
        return self.name.__str__()


class InventoryOtherName(models.Model):
    UNIT_CHOICES = (
        ('kg', 'KG'),
        ('ltr', 'LTR'),
        ('pcs', 'PCS')
    )
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_other_names')

    name = models.CharField(max_length=255)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=5)

    objects = models.QuerySet()

    def __str__(self):
        return self.name


class InventoryOtherIN(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_others_in')

    name = models.ForeignKey(InventoryOtherName, on_delete=models.CASCADE, related_name='inventory_others_in')
    quantity = models.FloatField()

    price = models.FloatField()
    date = models.DateField(default=now)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.QuerySet()

    def __str__(self):
        return self.name


class InventoryOtherOUT(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name='inventory_others_out')

    name = models.ForeignKey(InventoryOtherIN, on_delete=models.CASCADE, related_name='inventory_others_out')
    quantity = models.FloatField()
    date = models.DateField(default=now)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.QuerySet()

    def __str__(self):
        return self.name

    def in_stock(self):
        if self.name.quantity >= self.quantity:
            return self.name.quantity - self.quantity
        return 0
