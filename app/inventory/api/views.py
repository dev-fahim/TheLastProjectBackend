from rest_framework.views import APIView, Response
from inventory.api import serializers
from inventory import models
import utils
from django.db.models import Sum


class InventoryFoodNameListAPIView(utils.OwnListCreateAPIView):
    own_model = models.InventoryFoodName
    own_serializer_class = serializers.InventoryFoodNameSerializer


class InventoryFoodINListAPIView(utils.OwnListCreateAPIView):

    own_model = models.InventoryFoodIN
    own_serializer_class = serializers.InventoryFoodINSerializer


class InventoryFoodOUTListAPIView(utils.OwnListCreateAPIView):

    own_model = models.InventoryFoodOUT
    own_serializer_class = serializers.InventoryFoodOUTSerializer


class InventoryOtherNameListAPIView(utils.OwnListCreateAPIView):

    own_model = models.InventoryOtherName
    own_serializer_class = serializers.InventoryOtherNameSerializer


class InventoryOtherINListAPIView(utils.OwnListCreateAPIView):

    own_model = models.InventoryOtherIN
    own_serializer_class = serializers.InventoryOtherINSerializer


class InventoryOtherOUTListAPIView(utils.OwnListCreateAPIView):

    own_model = models.InventoryOtherOUT
    own_serializer_class = serializers.InventoryOtherOUTSerializer


class InStockFoodInStock(APIView):

    def get_queryset(self):
        food_in_stock = models.InventoryFoodIN\
            .objects\
            .filter(main_user_id=utils.get_main_user(self.request.user)) \
            .values('name__name', 'name__unit')\
            .annotate(
                in_stock=Sum('quantity') - Sum('inventory_foods_out__quantity')
                )
        return food_in_stock

    def get(self, *args, **kwargs):
        return Response(self.get_queryset())


class InStockOtherInStock(APIView):

    def get_queryset(self):
        food_in_stock = models.InventoryOtherIN\
            .objects\
            .filter(main_user_id=utils.get_main_user(self.request.user)) \
            .values('name__name', 'name__unit')\
            .annotate(
                in_stock=Sum('quantity') - Sum('inventory_others_out__quantity')
            )
        return food_in_stock

    def get(self, *args, **kwargs):
        return Response(self.get_queryset())


class InventoryFoodNameEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryFoodName
    own_serializer_class = serializers.InventoryFoodNameSerializer


class InventoryFoodINEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryFoodIN
    own_serializer_class = serializers.InventoryFoodINSerializer


class InventoryFoodOUTEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryFoodOUT
    own_serializer_class = serializers.InventoryFoodOUTSerializer


class InventoryOtherNameEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryOtherName
    own_serializer_class = serializers.InventoryOtherNameSerializer


class InventoryOtherINEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryOtherIN
    own_serializer_class = serializers.InventoryOtherINSerializer


class InventoryOtherOUTEditAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_model = models.InventoryOtherOUT
    own_serializer_class = serializers.InventoryOtherOUTSerializer
