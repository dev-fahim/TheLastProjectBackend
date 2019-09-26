import utils
from bill.api import serializers
from bill import models
from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class BillListAPIView(utils.OwnListCreateAPIView):

    own_serializer_class = serializers.BillSerializer
    own_model = models.Bill
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().prefetch_related('bill_data')


class BillRetrieveUpdateDestroyAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_serializer_class = serializers.BillSerializer
    own_model = models.Bill


class BillDataRetrieveUpdateDestroyAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_serializer_class = serializers.BillDataSerializer
    own_model = models.BillData
