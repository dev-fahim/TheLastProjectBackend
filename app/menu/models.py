from django.db import models
from profile_app.models import MainUserProfile

# Create your models here.


class Menu(models.Model):
    main_user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name="menus")

    name = models.CharField(max_length=255)

    price = models.FloatField()

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.QuerySet()

    def __str__(self):
        return self.name
