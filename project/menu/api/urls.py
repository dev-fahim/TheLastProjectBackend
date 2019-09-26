from django.urls import path
from menu.api import views

app_name = 'menu'

urlpatterns = [
    path('all/', views.MenuListCreateAPIView.as_view(), name="menu_all"),
    path('<int:pk>/', views.MenuListRetrieveUpdateDestroyAPIView.as_view(), name="menu_edit"),
]
