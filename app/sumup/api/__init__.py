from rest_framework.views import APIView
from bill.models import Bill, BillData
from utils import get_main_user
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
from django.db.models import OuterRef, Subquery, Sum, F, Value
import datetime

today = datetime.date.today()

app_name = 'sumup'


class TodaySells(APIView):
    def get(self, request, format=None):

        query = Bill.objects.filter(main_user=get_main_user(request.user))

        print(query)

        # bill = Bill.objects.filter(main_user=get_main_user(request.user))
        amount = []
        """
        for i in bill:
            bill_data = BillData.objects.filter(bill=i).select_related('menu').only('menu__price', 'discount')
            print(bill_data.query)
            for j in bill_data:
                total_price = j.menu.price * j.quantity
                total_price_discount = total_price * j.discount / 100
                amount.append(total_price - total_price_discount)
            
            bill_total_amount = 0.00
            for j in i.bill_data:
                bill_total_amount += j.quantity*(j.menu.price - (j.menu.price/100*j.discount))
            amount.append(bill_total_amount - (bill_total_amount*i.discount/100))
            
        """
        return Response({'total_sell': sum(amount)}, status=status.HTTP_200_OK)


# URL section

urlpatterns = [
    path('today/', TodaySells.as_view(), name="today_sell"),
]
