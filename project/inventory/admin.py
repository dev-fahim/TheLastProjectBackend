from django.contrib import admin
from inventory import models
# Register your models here.


admin.site.register(models.InventoryFoodName)
admin.site.register(models.InventoryFoodIN)
admin.site.register(models.InventoryFoodOUT)
admin.site.register(models.InventoryOtherName)
admin.site.register(models.InventoryOtherIN)
admin.site.register(models.InventoryOtherOUT)
