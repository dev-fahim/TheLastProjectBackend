from django.contrib import admin
from profile_app.models import MainUserProfile, ApplicationMonthlyPayment, SubUserProfile, Permission
# Register your models here.

admin.site.register(MainUserProfile)
admin.site.register(SubUserProfile)
admin.site.register(Permission)
admin.site.register(ApplicationMonthlyPayment)
