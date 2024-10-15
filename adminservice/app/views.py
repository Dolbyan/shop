from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .models import Items, Order, User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .utilities import S3Client, JWT, IsAuthenticatedJWT, KafkaService
from rest_framework import status

import logging
logger = logging.getLogger(__name__)


class LoginView(APIView):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        try:
            logger.info("HEHEH")
            email = request.POST.get("email")
            password = request.POST.get("password")
            logger.info(f"Email: {email}, Password: {password}")
            user = User.objects.filter(email=email).first()
            print(user)
            if user is None:
                raise AuthenticationFailed("User not found!")

            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password!")

            token = JWT.generate_token(user)
            print(token)

            response = redirect("admin_dashboard")
            response.set_cookie(key="jwt", value=token)
            return response
        except KeyError as e:
            return render(request, "login.html", {"error":f"Missing field: {str(e)}"})
        except AuthenticationFailed as e:
            return render(request, "login.html", {"error":str(e)})
        except Exception as e:
            return render(request, "login.html", {"error":str(e)})


class LogoutView(APIView):
    def get(self, request):
        try:
            response = Response()
            response.delete_cookie("jwt")
            response.data = {
                "message":"success"
            }
            return response
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        try:
            user = request.user
            if not user.is_staff:
                raise PermissionDenied("Unauthorized")

            total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
            total_orders = Order.objects.count()
            total_customers = Order.objects.values('user_id').distinct().count()
            total_products = Items.objects.count()

            today = timezone.now()
            last_week = today - timedelta(days=7)

            sales_last_week = Order.objects.filter(created_at__gte=last_week).aggregate(
                total_sales=Sum('total_amount'))['total_sales'] or 0

            orders_last_week = Order.objects.filter(created_at__gte=last_week).count()

            recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

            dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
            sales_chart_labels = [date.strftime('%Y-%m-%d') for date in dates]
            sales_chart_data = []

            for date in dates:
                daily_sales = Order.objects.filter(
                    created_at__date=date.date()
                ).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
                sales_chart_data.append(float(daily_sales))

            context = {
                'user':user,
                'total_sales':total_sales,
                'total_orders':total_orders,
                'total_customers':total_customers,
                'total_products':total_products,
                'sales_last_week':sales_last_week,
                'orders_last_week':orders_last_week,
                'recent_orders':recent_orders,
                'sales_chart_labels':sales_chart_labels,
                'sales_chart_data':sales_chart_data,
            }

            return render(request, 'admin_dashboard.html', context)
        except AuthenticationFailed as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"detail":str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPage(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        try:
            user = request.user
            if not user.is_staff:
                return Response({"detail":"Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

            if user.is_staff:
                items = Items.get_inv()
                return render(request, "inventory_edit.html", {"items":items, "user":user})
            else:
                print("ERROR")
        except AuthenticationFailed as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"detail":str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminInventoryView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        try:
            user = request.user
            if not user.is_staff:
                raise PermissionDenied("Unauthorized")
            items = Items.objects.all()
            return render(request, "admin_inventory.html", {"items":items, "user":user})
        except Exception as e:
            print(str(e))
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            if not user.is_staff:
                raise PermissionDenied("Unauthorized")

            action = request.POST.get("action")
            if action == "add":
                return self.add_item(request)
            elif action == "edit":
                return self.edit_item(request)
            elif action == "delete":
                return self.delete_item(request)
            else:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def add_item(self, request):
        name = request.POST.get("name")
        category = request.POST.get("category")
        description = request.POST.get("description")
        price = request.POST.get("price")
        amount = request.POST.get("amount")

        image = request.FILES.get("image")
        image_url = None
        image_name= ""
        if image:
            image_name = image.name
            s3 = S3Client()
            success = s3.upload_file(image)
            if success:
                image_url = f"https://{s3.bucket_name}.s3.amazonaws.com/{image_name}"
            else:
                image_url = None


        item = Items.objects.create(
            name=name,
            type=category,
            description=description,
            price=price,
            amount=amount,
            image=image_url,
            image_name=image_name
        )
        kafka_service = KafkaService()
        kafka_service.send_message('inventory_updates', 'create', 'Items', {
            'name':item.name,
            'category':item.type,
            'description':item.description,
            'price':item.price,
            'amount':item.amount,
            'image_url': item.image,
            'image_name': item.image_name,
            'source': 'admin'
        })

        return redirect('admin_inventory')

    def edit_item(self, request):
        item_id = request.POST.get("item_id")
        print(f"Received item_id: {item_id}")
        if not item_id:
            return Response({"detail":"Brak item_id w żądaniu"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item_id = int(item_id)
        except ValueError:
            return Response({"detail":"Nieprawidłowy item_id"}, status=status.HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Items, pk=item_id)

        name = request.POST.get("name")
        category = request.POST.get("category")
        description = request.POST.get("description")
        price = request.POST.get("price")
        amount = request.POST.get("amount")

        if name != '':
            item.name = name
        if category != '':
            item.type = category
        if description != '':
            item.description = description
        if price != '':
            item.price = float(price)
        if amount != '':
            item.amount = float(amount)

        image = request.FILES.get("image")
        if image:
            s3 = S3Client()
            success = s3.upload_file(image)
            if success:
                image_name = image.name
                image_url = f"https://{s3.bucket_name}.s3.amazonaws.com/{image_name}"
                item.image = image_url
                item.image_name = image_name
        item.save()
        kafka_service = KafkaService()
        kafka_service.send_message('inventory_updates', 'update', 'Items', {
            "id": item_id,
            "name": item.name,
            "category": item.type,
            "description": item.description,
            "price": item.price,
            "amount": item.amount,
            "image_url": item.image,
            "image_name": item.image_name,
            "source": "admin"
        })

        return redirect("admin_inventory")

    def delete_item(self, request):
        item_id = request.POST.get("item_id")
        item = get_object_or_404(Items, pk=item_id)
        item.delete()
        kafka_service = KafkaService()
        kafka_service.send_message('inventory_updates', 'delete', 'Items', {
            'id': item_id,
            'source':'admin'
        })

        return redirect('admin_inventory')


class AdminGetItemView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request, item_id):
        try:
            user = request.user
            if not user.is_staff:
                return JsonResponse({"detail":"Unauthorized"}, status=403)
            item = get_object_or_404(Items, pk=item_id)
            data = {
                "id":item.id,
                "name":item.name,
                "type":item.type,
                "description":item.description,
                "price":float(item.price),
                "amount":item.amount,
                "image":item.image,
            }
            return JsonResponse(data)
        except Exception as e:
            print(str(e))
            return JsonResponse({"detail":str(e)}, status=500)


class OrderListView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        try:
            search_query = request.GET.get('search', '')
            if request.user.is_staff:
                orders = Order.objects.all()
            if not request.user.is_staff:
                raise PermissionDenied("You do not have permission to view this")

            if search_query:
                orders = orders.filter(
                    Q(user__first_name__icontains=search_query) |
                    Q(user__last_name__icontains=search_query) |
                    Q(items__name__icontains=search_query)
                ).distinct()

            # Paginacja
            paginator = Paginator(orders, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                "orders":page_obj,
                "search_query":search_query,
            }
            return render(request, "orders.html", context)
        except AuthenticationFailed as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request, order_id):
        try:
            user = request.user
            order = get_object_or_404(Order, id=order_id)

            if not user.is_staff and order.user != user:
                raise PermissionDenied("You do not have permission to view this order")

            context = {
                'order':order,
                'user':user,
            }
            return render(request, 'order_detail.html', context)
        except AuthenticationFailed as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"detail":str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(str(e))
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
