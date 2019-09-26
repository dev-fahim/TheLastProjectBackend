from django.urls import path
from bill.api import views

app_name = 'bill'

urlpatterns = [
    path('all/', views.BillListAPIView.as_view(), name="bill_all"),
    path('<int:pk>/', views.BillRetrieveUpdateDestroyAPIView.as_view(), name="bill"),
    path('data/<int:pk>/', views.BillDataRetrieveUpdateDestroyAPIView.as_view(), name="bill_data"),
]
