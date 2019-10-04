from django.db import models
from profile_app.models import MainUserProfile
# Create your models here.


class ExtraExpend(models.Model):
    TYPE_CHOICES = (
        ("service", "Servicing"),
        ("clean", "Cleaning"),
        ("other", "Others")
    )
    user = models.ForeignKey(MainUserProfile, on_delete=models.CASCADE, related_name="extra_expends")
    type = models.CharField(max_length=55, choices=TYPE_CHOICES)

    description = models.TextField()

    date = models.DateField()

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
