import os
from faker import Faker
import random
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django

django.setup()

from inventory.models import *

inbound = InventoryFoodIN.objects.annotate(total=models.Sum('quantity'))
outgoing = InventoryFoodOUT.objects.annotate(models.Sum('quantity'))
names = InventoryFoodName.objects.all().annotate()

fakegen = Faker()
food_names = ['tacos', 'burger', 'charmin', 'noodles', 'coffee']
main_user = MainUserProfile.objects.get(pk=1)


def add_food_name():
    inventory_food_name = InventoryFoodName\
        .objects\
        .create(
            main_user=main_user,
            name=random.choice(food_names),
            unit='kg'
        )
    inventory_food_name.save()
    return inventory_food_name


def populate(n=10):
    for entry in range(n):
        inventory_food_name = add_food_name()
        date = fakegen.date_object()
        quantity = 5
        price = 100
        for in_entry in range(n):
            inbound = InventoryFoodIN\
                .objects\
                .create(
                    main_user=main_user,
                    name=inventory_food_name,
                    quantity=quantity,
                    price=price,
                    date=date,
                )
            InventoryFoodOUT\
                .objects\
                .create(
                    main_user=main_user,
                    name=inbound,
                    quantity=quantity-1,
                    date=date,
                )


def queries():

    food_out = InventoryFoodOUT\
        .objects\
        .values('name__name__name')\
        .annotate(total=models.Sum('quantity'))

    food_in = InventoryFoodIN\
        .objects.\
        values('name__name').\
        annotate(total=models.Sum('quantity'))
    start = time.time()
    food_in_stock = InventoryFoodIN\
        .objects.\
        values('name__name').\
        annotate(in_stock=models.Sum('quantity')-models.Sum('inventory_foods_out__quantity'))
    end = time.time()
    print((end-start))


if __name__ == '__main__':
    queries()
