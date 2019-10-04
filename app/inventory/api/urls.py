from django.urls import path, include
from inventory.api import views

app_name = 'inventory'

urlpatterns = [
    path('food/', include([
        path('name/', views.InventoryFoodNameListAPIView.as_view(), name='inventory_food_name'),
        path('name/<int:pk>/', views.InventoryFoodNameEditAPIView.as_view(), name='inventory_food_name_edit'),
        path('in/', views.InventoryFoodINListAPIView.as_view(), name='inventory_food_in'),
        path('in/<int:pk>/', views.InventoryFoodINEditAPIView.as_view(), name='inventory_food_in_edit'),
        path('out/', views.InventoryFoodOUTListAPIView.as_view(), name='inventory_food_out'),
        path('out/<int:pk>/', views.InventoryFoodOUTEditAPIView.as_view(), name='inventory_food_out_edit'),
        path('in-stock/', views.InStockFoodInStock.as_view())
    ]), name='inventory_food'),
    path('other/', include([
        path('name/', views.InventoryOtherNameListAPIView.as_view(), name='inventory_other_name'),
        path('name/<int:pk>/', views.InventoryOtherNameEditAPIView.as_view(), name='inventory_other_name_edit'),
        path('in/', views.InventoryOtherINListAPIView.as_view(), name='inventory_other_in'),
        path('in/<int:pk>/', views.InventoryOtherINEditAPIView.as_view(), name='inventory_other_in_edit'),
        path('out/', views.InventoryOtherOUTListAPIView.as_view(), name='inventory_other_out'),
        path('out/<int:pk>/', views.InventoryOtherOUTEditAPIView.as_view(), name='inventory_other_out_edit'),
        path('in-stock/', views.InStockOtherInStock.as_view())
    ]), name='inventory_other'),
]
