from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView,Home, InventoryView,ProfileView, ProductView, CartView,CartDelete, Checkout, OrderView, PaymentCancelledView, PaymentSuccessfulView, User_orders
from .administrator import AdminPage

urlpatterns = [
    path("home", Home.as_view(), name="home"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("user", UserView.as_view()),
    path("logout", LogoutView.as_view(), name='logout'),
    path("inventory", InventoryView.as_view(), name="inventory"),
    path("profile", ProfileView.as_view()),
    path("product/<int:product_id>", ProductView.as_view(), name="product"),
    path("cart", CartView.as_view(), name="cart"),
    path("cart_delete/<int:cart_item_id>/", CartDelete.as_view(), name="cart_item_delete"),
    path("admin_page", AdminPage.as_view(),name="admin_page"),
    path("checkout", Checkout.as_view(), name="checkout"),
    path("order", OrderView.as_view(), name="order"),
    path("payment_cancelled", PaymentCancelledView.as_view(), name="payment_cancelled"),
    path("payment_successful", PaymentSuccessfulView.as_view(), name="payment_successful"),
    path("user_orders", User_orders.as_view(), name="user_orders"),
]
