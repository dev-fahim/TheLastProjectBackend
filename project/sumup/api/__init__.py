from rest_framework.views import APIView
from bill.models import BillData, Bill
from utils import get_main_user
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
import datetime

today = datetime.date.today()

app_name = 'sumup'


class TodaySells(APIView):

    def get(self, request, format=None):
        print(today)
        values = []
        bill = Bill.objects.filter(main_user=get_main_user(request.user), added__date=today)
        for i in bill:
            print(i.bill_data)
            amount = sum([j.menu.price for j in i.bill_data])
            values.append(amount-amount*i.discount/100)
        return Response({'total_sell': sum(values)}, status=status.HTTP_200_OK)


urlpatterns = [
    path('today/', TodaySells.as_view(), name="today_sell"),
]
