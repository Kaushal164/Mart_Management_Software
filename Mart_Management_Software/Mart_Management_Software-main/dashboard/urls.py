from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:product_id>/', views.update_stock, name='update_stock'),
    path('sales/', views.sales_report, name='sales_report'),
    path('orders/', views.order_management, name='order_management'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
