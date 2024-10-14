from unittest.mock import MagicMock, patch
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from .models import User, Items, Order, Carts
from .utilities import JWT


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.add_new_user(
            name='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = JWT.generate_token(self.user)
        self.client.cookies['jwt'] = self.token

        self.item = Items.objects.create(
            name="Test Item",
            type="Electronics",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )
        self.cart_item = Carts.objects.create(
            user=self.user,
            product=self.item,
            quantity=1
        )

    @patch('stripe.checkout.Session.create')
    def test_checkout_view(self, mock_stripe_session_create):
        mock_stripe_session_create.return_value = MagicMock(url='http://test.checkout.url')
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://test.checkout.url')

class UserOrdersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.add_new_user(
            name='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        self.token = JWT.generate_token(self.user)
        self.client.cookies['jwt'] = self.token

        self.order = Order.objects.create(
            user=self.user,
            total_amount=200,
            quantity=2,
            payment_status=True
        )

    def test_user_orders_view(self):
        response = self.client.get(reverse('user_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_orders.html')
        self.assertContains(response, self.order.total_amount)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.add_new_user(
            name='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = JWT.generate_token(self.user)
        self.client.cookies['jwt'] = self.token

        # self.client.force_login(self.user)
        self.item = Items.objects.create(
            name="Test Item",
            type="Electronics",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )
        self.cart_item = Carts.objects.create(
            user=self.user,
            product=self.item,
            quantity=1
        )

    def test_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.assertContains(response, self.item.name)


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.item = Items.objects.create(
            name="Test Item",
            type="Electronics",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )

    def test_product_view(self):
        response = self.client.get(reverse('product', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_page.html')
        self.assertContains(response, self.item.name)


class InventoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.item = Items.objects.create(
            name="Test Item",
            type="Electronics",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )

    def test_inventory_view(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory.html')
        self.assertContains(response, self.item.name)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.add_new_user(
            name="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

    def test_login_view(self):
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('jwt', self.client.cookies)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        register_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'retype_password': 'password123',
            'terms': 'agree'
        }
        response = self.client.post(reverse('register'), data=register_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='johndoe@example.com').exists())


class AdminDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.add_new_user(
            name="adminuser",
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        self.token = JWT.generate_token(self.admin_user)

        self.client.cookies['jwt'] = self.token

        self.item = Items.objects.create(
            name="Test Item",
            type="Test Type",
            description="Test Description",
            price=100,
            amount=10,
            image=None,
            image_name="test_image.jpg"
        )

    def test_admin_dashboard_view(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_admin_inventory_view(self):
        print(f"Token: {self.token}")
        response = self.client.get(reverse('admin_inventory'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.item.name)

    def test_admin_inventory_add_item(self):
        new_item_data = {
            'name': 'New Item',
            'category': 'New Category',
            'description': 'New Description',
            'price': 150,
            'amount': 20,
            'image_name': 'new_image.jpg',
            'action': 'add'
        }
        response = self.client.post(reverse('admin_inventory'), data=new_item_data)
        self.assertEqual(response.status_code,  status.HTTP_302_FOUND)
        self.assertTrue(Items.objects.filter(name='New Item').exists())

    def test_admin_inventory_edit_item(self):

        update_data = {
            'name': 'Updated Item',
            'category': 'Updated Category',
            'description': 'Updated Description',
            'price': 200,
            'amount': 30,
            'action': 'edit',
            'item_id': self.item.id
        }
        response = self.client.post(reverse('admin_inventory'), data=update_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        updated_item = Items.objects.get(id=self.item.id)
        self.assertEqual(updated_item.name, 'Updated Item')
        self.assertEqual(updated_item.price, 200)

    def test_admin_inventory_delete_item(self):
        delete_data = {
            'action': 'delete',
            'item_id': self.item.id
        }
        response = self.client.post(reverse('admin_inventory'), data=delete_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(Items.objects.filter(id=self.item.id).exists())

