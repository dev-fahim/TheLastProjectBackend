from rest_framework import serializers
from inventory import models


class InventoryFoodNameSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='inventory:inventory_food_name_edit')

    class Meta:
        model = models.InventoryFoodName
        fields = '__all__'


class InventoryFoodINSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='inventory:inventory_food_in_edit')

    class Meta:
        model = models.InventoryFoodIN
        fields = '__all__'


class InventoryFoodOUTSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='inventory:inventory_food_out_edit')

    class Meta:
        model = models.InventoryFoodOUT
        fields = '__all__'

    # Todo: (Food) Add logic when out (in - out) >= 0 [create, update]


class InventoryOtherNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InventoryOtherName
        fields = '__all__'


class InventoryOtherINSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InventoryOtherIN
        fields = '__all__'


class InventoryOtherOUTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InventoryOtherOUT
        fields = '__all__'

    # Todo: (Other) Add logic when out (in - out) >= 0 [create, update]
