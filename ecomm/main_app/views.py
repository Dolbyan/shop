from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User, Items, Carts, Order
from .utilities import JWT, IsAuthenticatedJWT, KafkaService
from .serializers import UserSerializer
from django.conf import settings
from django.http import HttpResponse
import stripe
from rest_framework import status



class InventoryView(APIView):
    def get(self, request):
        try:
            items = Items.get_inv()
            return render(request, "inventory.html", {"items": items})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductView(APIView):
    def get(self, request, product_id):
        try:
            items = Items.get_inv()
            return render(request, "product_page.html", {"items": items, "product_id": product_id})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class User_orders(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def get(self, request):
        try:
            user = request.user
            user_orders = Order.objects.filter(user=user)
            return render(request, "user_orders.html", {"user_orders":user_orders})
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        try:
            user = request.user
            cart_items = Carts.objects.filter(user=user)
            total_amount = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
            return render(request, "cart.html", {"cart_data": cart_items, "total_amount": total_amount})
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            product_id = request.data.get("product_id")
            quantity = request.data.get("amount")

            if not product_id or not quantity:
                raise ValidationError("Product ID and amount are required")

            try:
                quantity = int(quantity)
            except ValueError:
                raise ValidationError("Amount must be an integer.")

            product = Items.objects.get(id=product_id)
            cart_item = Carts.objects.filter(user=user, product=product).first()

            if cart_item:
                if cart_item.quantity < product.amount:
                    cart_item.quantity += quantity
                    cart_item.save()
            else:
                Carts.objects.create(user=user, product=product, quantity=quantity)
            return redirect("http://127.0.0.1:8000/api/cart")
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Items.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Checkout(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def post(self, request):
        try:
            user = request.user

            if user.is_authenticated:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                cart_items = Carts.objects.filter(user=user)
                total_amount = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
                shipping = 20
                line_items = [{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int((cart_item.product.price * cart_item.quantity + 20) * 100),
                        "product_data": {
                            "name": cart_item.product.name,
                            "description": cart_item.product.description,
                        },
                    },
                    "quantity": 1,
                } for cart_item in cart_items]

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=line_items,
                    mode="payment",
                    customer_creation="always",
                    success_url=settings.REDIRECT_DOMAIN + "payment_successful?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=settings.REDIRECT_DOMAIN + "payment_cancelled",
                )
                return redirect(checkout_session.url, code=303)

            else:
                return redirect("login")
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessfulView(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def get(self, request):
        try:
            session_id = request.GET.get("session_id", None)
            user = request.user
            cart_items = Carts.objects.filter(user=user)
            if session_id and user.is_authenticated:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                session = stripe.checkout.Session.retrieve(session_id)
                print(session, "SESSION PAYMENTVIEW")
                customer = stripe.Customer.retrieve(session.customer)
                print(customer, "CUSTOMER PAYMENTVIEW")
                user = user
                order = Order.objects.create(
                    user=user,
                    total_amount=session.amount_total,
                    payment_status=True,
                )

                for cart_item in cart_items:
                    order.items.add(cart_item.product)
                kafka_service = KafkaService()
                for cart_item in cart_items:
                    kafka_service.send_message('inventory_updates', 'update', 'Items', {
                        "name": cart_item.product.id,
                        "amount": cart_item.quantity,
                        "source" : "user"
                    })
                cart_items.delete()
                return render(request, "success.html", {"customer": customer})
            else:
                return HttpResponse("Error: no session payment id")
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return HttpResponse("Error: {}".format(e))

class PaymentCancelledView(APIView):
    def get(self, request):
        return render(request, "cancel.html")


class CartDelete(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def post(self, request, cart_item_id):
        try:
            user = request.user
            cart_item = get_object_or_404(Carts, id=cart_item_id, user=user)
            cart_item.delete()
            return render(request, "cart.html")
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Carts.DoesNotExist:
            return Response({"detail": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderView(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def get(self, request):
        return render(request, "checkout.html")

    def post(self, request):
        try:
            user = request.user
            cart_item = Carts.objects.filter(user=user)
            line_items = []
            total_amount = 0
            order_items = []

            for item in cart_item:
                line_item = {
                    "price": item.product.price,
                    "quantity": item.quantity
                }
                line_items.append(line_item)
                total_amount += item.product.price * item.quantity
                order_items.append(item.product)

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/api/checkout/success/'),
                cancel_url=request.build_absolute_uri('/api/checkout/cancel/'),
            )

            return redirect(checkout_session.url)
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Payment(APIView):
    def post(self, request):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=1,
                currencty="usd",
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(APIView):
    def get(self, request):
        return render(request, "register-v2.html")

    def post(self, request):
        try:
            name = request.data["name"]
            email = request.data["email"]
            password = request.data["password"]
            retype_password = request.data["retype_password"]

            print(name, email, password, retype_password)

            if password != retype_password:
                return render(request, "start_file.html", {"error": "Passwords don't match"})
            if User.objects.filter(email=email).exists():
                return render(request, "register-v2.html", {"error": "Email already exists"})
            if User.objects.filter(name=name).exists():
                return render(request, "register-v2.html", {"error": "Username already exists"})

            user = User.add_new_user(name=name, email=email, password=password)
            print(user)
            token = JWT.generate_token(user)
            response = redirect("http://127.0.0.1:8000/api/home")
            response.set_cookie(key="jwt", value=token)
            return response
        except KeyError as e:
            return render(request, "register-v2.html", {"error": f"Missing field: {str(e)}"})
        except ValueError as e:
            return render(request, "register-v2.html", {"error": str(e)})
        except Exception as e:
            return render(request, "register-v2.html", {"error": str(e)})


class LoginView(APIView):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]

            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed("User not found!")

            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password!")

            token = JWT.generate_token(user)

            # response = render(request, "inventory.html")
            response = redirect("inventory")
            response.set_cookie(key="jwt", value=token)
            return response
        except KeyError as e:
            return render(request, "login.html", {"error": f"Missing field: {str(e)}"})
        except AuthenticationFailed as e:
            return render(request, "login.html", {"error": str(e)})
        except Exception as e:
            return render(request, "login.html", {"error": str(e)})


class UserView(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except AuthenticationFailed as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Home(APIView):
    permission_classes = [IsAuthenticatedJWT]
    def get(self, request):
        try:
            user = request.user
            items = Items.get_inv()
            return render(request, "index.html", {"items": items, "user": user})
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    def get(self, request):
        try:
            response = Response()
            response.delete_cookie("jwt")
            response.data = {
                "message": "success"
            }
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(APIView):

    def get(self, request):
        try:
            user_view = UserView()
            user = user_view.get(request)
            print(user, "?????")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
