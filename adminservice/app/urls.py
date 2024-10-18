from django.urls import path
from .views import OrderListView, AdminDashboardView, OrderDetailView, AdminInventoryView, AdminGetItemView, LoginView, LogoutView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name='logout'),
    path("admin/orders", OrderListView.as_view(), name="orders"),
    path("admin/orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
    path("admin/dashboard", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/inventory", AdminInventoryView.as_view(), name="admin_inventory"),
    path("admin/get_item/<int:item_id>/", AdminGetItemView.as_view(), name="admin_get_item"),
]
